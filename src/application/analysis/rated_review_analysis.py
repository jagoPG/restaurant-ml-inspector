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

from textblob import TextBlob

from src.application.analysis.evaluated_word import EvaluatedWord


class RatedReviewAnalysis(object):
    """
    Reads the score of previously tagged English and Spanish results, gather
    all results in a word dictionary with its score and the appearances
    references.
    """

    def __init__(self, keyword_repository, restaurants):
        self._keyword_repository = keyword_repository
        self._restaurants = restaurants
        self._es_words = {}
        self._en_words = {}

    def analyse(self):
        """
        Analyses the reviews that have been set
        """
        self.__gather_tagged_reviews(self._restaurants)

    def get_english_results(self):
        """
        :return: Rated English results
        :returns: EvaluatedWord
        """
        return self._en_words

    def get_spanish_results(self):
        """
        :return: Rated Spanish results
        :returns: EvaluatedWord
        """
        return self._es_words

    def __gather_tagged_reviews(self, restaurants):
        for restaurant in restaurants:
            reviews = restaurant.get_reviews()
            self.__filter_tagged_reviews(reviews)

    def __filter_tagged_reviews(self, reviews):
        for review in reviews:
            if review.sentiment is None:
                continue
            self.__analyse_phrase(
                review.review_body, review.sentiment, review.reference
            )

    def __analyse_phrase(self, phrase, sentiment, review_id):
        phrase = TextBlob(phrase)
        language = phrase.detect_language()
        for word in phrase.words:
            if not self.__is_keyword(word, language):
                continue
            self.__add_word_analysis(word, language, sentiment, review_id)

    def __is_keyword(self, word, language):
        return self._keyword_repository.get_of_name(word, language) is not None

    def __add_word_analysis(self, word, language, karma, review_id):
        if language == 'es':
            word_list = self._es_words
        else:
            word_list = self._en_words
        if word in word_list:
            word = word_list[word]
            word.add_karma(karma)
            if review_id not in word.appearances:
                word.add_appearance(review_id)
        else:
            word = EvaluatedWord(word, karma, [review_id])
            word_list[word.word] = word
