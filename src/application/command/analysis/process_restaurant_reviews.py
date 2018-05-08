#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
Copyright 2017-2018 Jagoba Pérez-Gómez

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging

from tabulate import tabulate
from textblob import TextBlob

from src.application.analysis.english_analysis import EnglishAnalysis
from src.application.analysis.evaluated_word import EvaluatedWord
from src.application.analysis.rated_review_analysis import RatedReviewAnalysis
from src.domain.exception import ReviewIsNotAnalysable
from src.domain.model import KeyPoint
from src.infrastructure.dependency_injector import Dependency


class ProcessRestaurantReviewsCommand(object):
    """
    Processes all the reviews from the restaurant for finding the strong and
    improvements points from the business.
    """

    def __init__(self, project_id):
        self.project_id = project_id


class ProcessRestaurantReviews(Dependency):
    def __init__(self):
        self.project_repository = None
        self.keyword_repository = None
        self.review_repository = None
        self.analysis_repository = None
        self.point_repository = None
        self.spanish_analyser = None
        self.synonym_reducer = None

        self._english_reviews = []
        self._spanish_reviews = []

    def invoke(self, command):
        self.__clean_vars()
        project = self.__retrieve_project(command.project_id)
        analysis = project.get_analysis()
        restaurants = self.__retrieve_restaurants(project)

        # Filter reviews and classify reviews
        self.__filter_not_tagged_reviews(restaurants)
        tagged_spanish_results, tagged_english_results = \
            self.__filter_tagged_reviews(restaurants)

        # Analyse reviews
        english_results = self.__process_english_reviews(self._english_reviews)
        spanish_results = self.__process_spanish_reviews(self._spanish_reviews)

        # Perform word equivalence
        logging.debug(
            english_results,
            spanish_results,
            tagged_english_results,
            tagged_spanish_results
        )
        english_results = self.__mix_results(
            english_results, tagged_english_results
        )
        spanish_results = self.__mix_results(
            spanish_results, tagged_spanish_results
        )

        # Mix depending on synonyms
        self.synonym_reducer.clean()
        self.synonym_reducer.reduce(english_results, 'en')
        self.synonym_reducer.reduce(spanish_results, 'es')

        # Summarize data
        self.__store_conclusions(analysis, self.synonym_reducer.words)

    def __clean_vars(self):
        self._english_reviews = []
        self._spanish_reviews = []

    def __retrieve_project(self, project_id):
        return self.project_repository.get_of_id(project_id)

    @staticmethod
    def __retrieve_restaurants(project):
        restaurants = []
        for restaurant in project.restaurants:
            restaurants.append(restaurant)
        return restaurants

    def __filter_tagged_reviews(self, restaurants):
        tagged_review_analysis = RatedReviewAnalysis(
            self.keyword_repository, restaurants
        )
        tagged_review_analysis.analyse()
        return (
            tagged_review_analysis.get_spanish_results(),
            tagged_review_analysis.get_english_results()
        )

    def __filter_not_tagged_reviews(self, restaurants):
        for restaurant in restaurants:
            self.__process_restaurants_in_social_network(restaurant)

    def __process_restaurants_in_social_network(self, restaurant):
        logging.debug(
            'Analise %s social network reviews'
            % restaurant.source_network.single().name
        )
        reviews = restaurant.get_reviews()
        for review in reviews:
            if review.is_spam or review.sentiment is not None:
                continue
            try:
                self.__classify_review(review)
            except ReviewIsNotAnalysable:
                self.__set_review_not_analysable(review)

    def __classify_review(self, review):
        body = review.review_body
        self.__check_review_is_long_enough(body)
        body = TextBlob(review.review_body)
        language = body.detect_language()
        self.__check_review_language_is_supported(language)
        if language == 'en':
            self._english_reviews.append(review)
        elif language == 'es':
            self._spanish_reviews.append(review)

    @staticmethod
    def __check_review_is_long_enough(body):
        if not len(body) > 3:
            raise ReviewIsNotAnalysable()

    @staticmethod
    def __check_review_language_is_supported(language):
        if language not in ['en', 'es']:
            raise ReviewIsNotAnalysable()

    def __process_english_reviews(self, english_reviews):
        analysis = EnglishAnalysis(
            self.keyword_repository, english_reviews
        )
        analysis.analyse()
        return analysis.get_results()

    def __process_spanish_reviews(self, spanish_reviews):
        try:
            self.spanish_analyser.analyse(spanish_reviews)
        except ValueError as exception:
            logging.info('%s' % exception.__str__())
        return self.spanish_analyser.get_results()

    def __set_review_not_analysable(self, review):
        review.is_spam = True
        self.review_repository.persist(review)

    def __mix_results(self, *results):
        lang_words = {}
        for result in results:
            for word, data in result.items():
                self.__store_in_result_list(word, data, lang_words)
        return lang_words

    @staticmethod
    def __store_in_result_list(word, data, lang_words):
        word = word.lower()
        if word in lang_words:
            word = lang_words[word]
            word.add_karma(data.karma)
            for review_id in data.appearances:
                if review_id not in word.appearances:
                    word.add_appearance(review_id)
        else:
            word = EvaluatedWord(word, data.karma, data.appearances)
            lang_words[word.word] = word

    def __store_conclusions(self, analysis, final_report):
        karma = 0
        for word, item in final_report.items():
            self.__create_point_instance(word, item, analysis)

        #  Show conclusions and CALCULATE KARMA
        header = ['Word', 'Karma', 'Review Appearances']
        data = []
        for word, item in final_report.items():
            current = list()
            current.append(word)
            current.append(final_report[word].karma)
            current.append(final_report[word].count)
            data.append(current)
            karma = (karma + float(final_report[word].karma)) / 2
        logging.debug(tabulate(data, header))

        # Store karma
        analysis.karma = karma
        self.analysis_repository.persist(analysis)

    def __create_point_instance(self, word, item, analysis):
        point = KeyPoint(
            identifier=word,
            karma=item.karma,
            analysis=analysis
        )
        self.point_repository.persist(point)
        analysis.add_key_point(point)
        self.analysis_repository.persist(analysis)
        self.__connect_points_to_reviews(item, point)

    def __connect_points_to_reviews(self, item, point):
        for review in item.appearances:
            review = self.__retrieve_review_of_id(review)
            if review is None:
                continue
            point.add_review(review)

    def __retrieve_review_of_id(self, review_id):
        return self.review_repository.get_of_id(review_id)
