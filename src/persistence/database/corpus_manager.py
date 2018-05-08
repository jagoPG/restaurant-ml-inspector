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

from src.application.analysis.corpus_reader import GastronomicCsvCorpusReader
from src.application.analysis.train_corpus import TrainCorpus
from src.infrastructure.dependency_injector import Dependency


class CorpusManager(Dependency):
    """
    Loads the corpus used for analysing reviews. Custom corpus and already
    tagged reviews from database are used as source.
    """

    def __init__(self):
        self._review_repository = None
        self._corpus_reader = GastronomicCsvCorpusReader()
        self._train_corpus = TrainCorpus()

    def initialise(self):
        self.load_corpus()

    def load_corpus(self):
        self.__read_corpus_file()
        self.__retrieve_stored_opinions()

    def get_training_set(self):
        return self._train_corpus

    def __read_corpus_file(self):
        phrases, sentiments = self._corpus_reader.parse(
            './src/application/data/corpus/60_corpus.csv'
        )
        self._train_corpus.content = phrases
        self._train_corpus.polarity = sentiments

    def __retrieve_stored_opinions(self):
        reviews = self._review_repository.get_scored_reviews()
        for review in reviews:
            self._train_corpus.content.append(review.review_body)
            self._train_corpus.polarity.append(review.sentiment)
