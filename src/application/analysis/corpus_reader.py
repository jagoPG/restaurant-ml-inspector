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

from xml.dom import minidom
import csv


class CorpusReader(object):
    """
    This class defines the methods a corpus reader must to fulfil for being
    used by the analysis tools
    """

    def parse(self, file):
        """
        Reads a file and converts its contents to an array with the trained
        phrases and  another array with the polarity of that phrases.

        :param file: The file to be read
        :return: array of phrases and an array of sentiments
        """
        raise NotImplementedError


class CorpusReaderNotConfigured(Exception):
    """
    An analyser instance has not set up a corpus reader
    """


class GastronomicCsvCorpusReader(CorpusReader):
    """
    This class loads the custom corpus created for analysing reviews from
    restaurants.
    """

    def parse(self, file):
        phrases = []
        polarities = []
        with open(file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                polarities.append(
                    self.__normalize_polarity(row['sentiment'])
                )
                phrases.append(row['phrase'])
        return phrases, polarities

    @staticmethod
    def __normalize_polarity(polarity):
        if polarity == 'N+':
            return -2
        elif polarity == 'N':
            return -1
        elif polarity == 'P':
            return 1
        elif polarity == 'P+':
            return 2
        else:
            return 0
