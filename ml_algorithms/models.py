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
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVR, LinearSVC, SVC
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from ml_algorithms.dense_transformer import DenseTransformer
from src.application.analysis.corpus_reader import GastronomicCsvCorpusReader
from src.application.analysis.train_corpus import TrainCorpus
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def tokenize(phrase):
    non_words = list(punctuation)
    non_words.extend(['¿', '¡', '\n', '…'])
    non_words.extend(map(str, range(10)))
    ''.join([char for char in phrase if char not in non_words])
    tokens = word_tokenize(phrase, language='spanish')
    stemmer = SnowballStemmer('spanish')
    stems = list(map(stemmer.stem, tokens))
    return stems


def normalize_to_tagged(score):
    if score >= .5:
        return 2
    elif score > 0:
        return 1
    elif score <= -.5:
        return -2
    elif score < 0:
        return 1
    return 0


class ModelTest(object):
    def __init__(self):
        self.corpus_reader = None
        self.train_corpus = None
        self.stop_words = stopwords.words('spanish')
        self.vectorizer = CountVectorizer(
            analyzer='word',
            tokenizer=tokenize,
            lowercase=True,
            stop_words=self.stop_words
        )

    def prepare_data_set(self):
        self.corpus_reader = GastronomicCsvCorpusReader()
        # corpus_reader = TassXmlCorpusReader()

        self.train_corpus = TrainCorpus()
        phrases, sentiments = self.corpus_reader.parse(
            './src/application/data/corpus/restaurant_corpus.csv'
        )
        # phrases, sentiments = self.corpus_reader.parse(
        #     './src/application/data/corpus/60_corpus.csv'
        # )
        # phrases, sentiments = corpus_reader.parse(
        #     './src/application/data/corpus/general-tweets-train-tagged.xml'
        # )
        # phrases, sentiments = corpus_reader.parse(
        #     './src/application/data/corpus/politics2013-tweets-test-tagged.xml'
        # )
        self.train_corpus.content = phrases
        self.train_corpus.polarity = sentiments

    def test_gaussian_nb(self):
        pipeline = Pipeline([
            ('vect', self.vectorizer),
            ('transformer', DenseTransformer()),
            ('cls', GaussianNB())
        ])

        X = self.train_corpus.content
        Y = self.train_corpus.polarity

        x_train, x_test, y_train, y_test = train_test_split(
            X, Y, random_state=None
        )
        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_test)
        self.__display_results(y_test, y_pred)

    def test_svc(self):
        pipeline = Pipeline([
            ('vect', self.vectorizer),
            ('cls', SVC(
                kernel='poly',
                C=0.9,
                gamma=1,
                random_state=None
            ))
        ])

        X = self.train_corpus.content
        Y = self.train_corpus.polarity

        x_train, x_test, y_train, y_test = train_test_split(
            X, Y, random_state=None
        )
        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_test)

        # Only with SVR: Data conversion from continuous to discrete is required
        index = 0
        results = list()
        while index < len(y_pred):
            result = normalize_to_tagged(y_pred[index])
            results.append(int(result))
            index += 1
        self.__display_results(y_test, results)

    def test_svr(self):
        pipeline = Pipeline([
            ('vect', self.vectorizer),
            ('cls', SVR())
        ])

        X = self.train_corpus.content
        Y = self.train_corpus.polarity

        x_train, x_test, y_train, y_test = train_test_split(
            X, Y, random_state=None
        )
        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_test)

        # Only with SVR: Data conversion from continuous to discrete is required
        index = 0
        results = list()
        while index < len(y_pred):
            result = normalize_to_tagged(y_pred[index])
            results.append(int(result))
            index += 1
        self.__display_results(y_test, results)

    def test_linear(self):
        pipeline = Pipeline([
            ('vect', self.vectorizer),
            ('cls', LinearSVC())
        ])

        X = self.train_corpus.content
        Y = self.train_corpus.polarity

        x_train, x_test, y_train, y_test = train_test_split(
            X, Y, random_state=None
        )

        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_test)
        self.__display_results(y_test, y_pred)

    def test_logistic_regression(self):
        pipeline = Pipeline([
            ('vect', self.vectorizer),
            ('cls', LogisticRegression())
        ])

        X = self.train_corpus.content
        Y = self.train_corpus.polarity

        x_train, x_test, y_train, y_test = train_test_split(
            X, Y, random_state=None
        )

        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_test)
        self.__display_results(y_test, y_pred)

    def test_knn_classifier(self):
        pipeline = Pipeline([
            ('vect', self.vectorizer),
            ('cls', KNeighborsClassifier())
        ])

        X = self.train_corpus.content
        Y = self.train_corpus.polarity

        x_train, x_test, y_train, y_test = train_test_split(
            X, Y, random_state=None
        )

        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_test)
        self.__display_results(y_test, y_pred)

    def test_decision_tree_classifier(self):
        pipeline = Pipeline([
            ('vect', self.vectorizer),
            ('cls', DecisionTreeClassifier())
        ])

        X = self.train_corpus.content
        Y = self.train_corpus.polarity

        x_train, x_test, y_train, y_test = train_test_split(
            X, Y, random_state=None
        )

        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_test)
        self.__display_results(y_test, y_pred)

    @staticmethod
    def __display_results(y_test, y_pred):
        print(
            classification_report(y_test, y_pred)
        )
