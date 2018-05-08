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

from textblob import TextBlob

from src.application.analysis.evaluated_word import EvaluatedWord


class EnglishAnalysis(object):
    """
    Receives an array of reviews and analyses them. The results are stored in
    an array of words that matches with the keyword repository list. A global
    score of all reviews is stored in the $karma$ variable.
    """

    def __init__(self, keyword_repository, reviews):
        self._keyword_repository = keyword_repository
        self._reviews = reviews
        self._words = {}
        self._karma = 0

    def analyse(self):
        """
        Analyses the reviews that have been set
        """
        for review in self._reviews:
            self.__process_english_review(review)
    
    def get_results(self):
        """
        :return: Gets the words analysis result
        :returns: EvaluatedWord
        """
        return self._words

    def get_karma(self):
        """
        :return: Gets the global score of all reviews
        :returns: float
        """
        return self._karma

    def __process_english_review(self, review):
        body = TextBlob(review.review_body)
        for sentence in body.sentences:
            logging.debug('Polarity: %s' % sentence.sentiment.polarity)
            self._karma = (sentence.sentiment.polarity + self._karma) / 2
        for sentence in body.sentences:
            for smaller_word in sentence.split(' '):
                logging.debug('Word: %s' % smaller_word)
                self.__process_word(smaller_word, sentence.sentiment.polarity, review.reference)

    def __process_word(self, word, karma, review_id):
        word = word.lower()
        if not self.__is_keyword(word):
            return
        if word in self._words:
            word = self._words[word]
            word.add_karma(karma)
            if review_id not in word.appearances:
                word.add_appearance(review_id)
        else:
            word = EvaluatedWord(word, karma, [review_id])
            self._words[word.word] = word

    def __is_keyword(self, word):
        return self._keyword_repository.get_of_name(word, 'en') is not None
