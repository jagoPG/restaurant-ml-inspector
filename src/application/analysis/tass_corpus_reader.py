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
from src.application.analysis.corpus_reader import CorpusReader


class TassXmlCorpusReader(CorpusReader):
    """
    This class loads the corpus provided by the SEPLN
    """

    def parse(self, filename):
        phrases = []
        polarities = []
        xml_corpus = open(filename, 'r')
        xml_corpus = minidom.parse(xml_corpus)
        tweets = xml_corpus.getElementsByTagName('tweets')[
            0].getElementsByTagName('tweet')
        for tweet in tweets:
            content, polarity = self.__parse_tweet(tweet)
            polarity = self.__normalize_polarity(polarity)
            if polarity is None or content is None:
                continue
            phrases.append(content)
            polarities.append(polarity)
        return phrases, polarities

    @staticmethod
    def __parse_tweet(tweet):
        content = tweet.getElementsByTagName('content')[0]
        polarity = tweet.getElementsByTagName('polarity')[0]
        if not content.firstChild:
            return None, None
        if not polarity:
            return None, None
        content = content.firstChild.data
        polarity = polarity.getElementsByTagName('value')[0].firstChild.data
        return content, polarity

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
