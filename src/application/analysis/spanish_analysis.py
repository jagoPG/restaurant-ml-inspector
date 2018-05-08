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

from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import SnowballStemmer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from src.application.analysis.evaluated_word import EvaluatedWord
from src.infrastructure.dependency_injector import Dependency


class SpanishAnalysis(Dependency):
    """
    Analyses the Spanish reviews and store in the instance the global score of
    the reviews and the keywords detected along with the score of individual
    keywords.
    """

    def __init__(self):
        self._keyword_repository = None
        self._corpus_manager = None

        self._non_words = list(punctuation)
        self._non_words.extend(['¿', '¡', '\n', '…'])
        self._non_words.extend(map(str, range(10)))
        self._stop_words = stopwords.words('spanish')
        self._stemmer = SnowballStemmer('spanish')
        self._analyser = None

        self._karma = 0
        self._words = {}

    def initialise(self):
        """
        Trains the SVM with the available data in the database and in the
        custom corpus.
        """
        self.set_up()

    def set_up(self):
        train_corpus = self._corpus_manager.get_training_set()
        self._analyser = Pipeline([
            ('vect', CountVectorizer(
                analyzer='word',
                tokenizer=self.__tokenise,
                stop_words=self._stop_words,
                lowercase=True,
                max_features=1000,
                min_df=50,
                max_df=1.9,
                ngram_range=(1, 1)
            )),
            ('cls', LogisticRegression())
        ])
        self._analyser.fit(train_corpus.content, train_corpus.polarity)

    def analyse(self, reviews):
        """
        Analyses the reviews that have been set
        :param reviews: Dictionary with the following format: {
            'review': 'string', 'identifier': 'string
        '}
        """
        if self._analyser is None:
            raise ModelNotTrained
        self.__clean_vars()
        bodies = self.__extract_review_body(reviews)
        predictions = self._analyser.predict(bodies)
        predictions = list(map(self.__normalize_prediction, predictions))
        self.__calculate_word_polarity(reviews, predictions)
        self.__calculate_global_karma(predictions)

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

    def __clean_vars(self):
        self._karma = 0
        self._words = {}

    @staticmethod
    def __extract_review_body(reviews):
        bodies = []
        for review in reviews:
            bodies.append(review.review_body)
        return bodies

    def __tokenise(self, phrase):
        phrase = self.__remove_non_words_from_phrase(phrase)
        tokens = word_tokenize(phrase, language='spanish')
        stems = self.__stem_tokens(tokens)
        return stems

    def __remove_non_words_from_phrase(self, phrase):
        return ''.join(
            [char for char in phrase if char not in self._non_words]
        )

    def __stem_tokens(self, tokens):
        stem_words = map(self._stemmer.stem, tokens)
        return list(stem_words)

    @staticmethod
    def __normalize_prediction(prediction):
        if prediction == -2:
            return -1
        elif prediction == -1:
            return -0.5
        elif prediction == 1:
            return 0.5
        elif prediction == 2:
            return 1
        else:
            return 0

    def __calculate_word_polarity(self, reviews, predictions):
        index = 0
        for review in reviews:
            phrase = review.review_body
            phrase = self.__remove_non_words_from_phrase(phrase)
            words = phrase.split(u' ')
            for word in words:
                self.__process_word(word, predictions[index],
                                    reviews[index].reference)
            index += 1

    def __process_word(self, word, karma, review_id):
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
        return len(self._keyword_repository.get_word_like(word, 'es')) > 0

    def __calculate_global_karma(self, predictions):
        self._karma = 0
        for prediction in predictions:
            self._karma = (self._karma + prediction) / 2


class ModelNotTrained(Exception):
    """
    The analyser has not being trained
    """
