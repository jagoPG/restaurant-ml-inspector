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
import os
from src.infrastructure.dependency_injector import Dependency
from src.domain.model import Keyword
from xml.dom import minidom


class KeywordLoader(Dependency):
    """
    Loads the list of keywords that is stored in the 'restaurant_keywords.xml'
    file into the database.
    """

    def __init__(self):
        self.keyword_repository = None
        self.keyword_xml_file = None
        self.synonyms_xml_file = None
        self._keywords = {}
        self._synonyms = {}

    def execute(self):
        self.__read_keyword_xml_file()
        self.__read_synonyms_xml_file()
        self.__record_words()
        self.__link_synonyms('es')
        self.__link_synonyms('en')
        self.__link_language()

    def __read_keyword_xml_file(self):
        if not os.path.isfile(self.keyword_xml_file):
            logging.error('file \'%s\' does not exist' % self.keyword_xml_file)
            return
        xml_file = open(self.keyword_xml_file, mode='r+', encoding='utf-8')
        document = minidom.parse(xml_file)
        for keyword in document.documentElement.getElementsByTagName('keyword'):
            identifier = keyword.getAttribute('identifier')
            self.__parse_xml_keyword(identifier, keyword)
        xml_file.close()

    def __parse_xml_keyword(self, identifier, keyword_node):
        translations = {}
        for translation in keyword_node.getElementsByTagName('word'):
            lang = translation.getAttribute('lang')
            word = translation.firstChild.nodeValue
            translations[lang] = word
        self._keywords[identifier] = translations

    def __read_synonyms_xml_file(self):
        if not os.path.isfile(self.synonyms_xml_file):
            logging.error('file \'%s\'does not exist' % self.synonyms_xml_file)
            return
        xml_file = open(self.synonyms_xml_file, mode='r+', encoding='utf-8')
        document = minidom.parse(xml_file)
        for keyword in document.documentElement.getElementsByTagName('synonym'):
            identifier = keyword.getAttribute('identifier')
            values = []
            for value in keyword.getElementsByTagName('keyword'):
                values.append(value.firstChild.nodeValue)
            self._synonyms[identifier] = values
        xml_file.close()

    def __record_words(self):
        for key, item in self._keywords.items():
            for lang, word in item.items():
                keyword = self.keyword_repository.get_of_name(word, lang)
                if keyword:
                    continue
                keyword = Keyword(
                    file_reference=key,
                    word=word,
                    language=lang
                )
                self.keyword_repository.persist(keyword)

    def __link_synonyms(self, language):
        for key, items in self._synonyms.items():
            self.__link_all_words(items, language)

    def __link_all_words(self, items, language):
        i = 0
        j = 0
        while i < len(items):
            while j + 1 < len(items):
                if language not in self._keywords[items[i]] \
                        or language not in self._keywords[items[j + 1]]:
                    j += 1
                    continue
                word_a = self._keywords[items[i]][language]
                word_b = self._keywords[items[j + 1]][language]
                word_a = self.keyword_repository.get_of_name(word_a, language)
                word_b = self.keyword_repository.get_of_name(word_b, language)
                word_a.add_synonym(word_b)
                self.keyword_repository.persist(word_a)
                self.keyword_repository.persist(word_b)
                logging.debug('Links %s with %s' % (word_a, word_b))
                j += 1
            i += 1

    def __link_language(self):
        for key, word in self._keywords.items():
            if 'en' not in word or 'es' not in word:
                continue
            word_es = self.keyword_repository.get_of_name(word['en'], 'en')
            word_en = self.keyword_repository.get_of_name(word['es'], 'es')
            word_es.add_translation(word_en)
            self.keyword_repository.persist(word_es)
            self.keyword_repository.persist(word_en)
            logging.debug(
                'Link translation %s with %s' % (word_es.word, word_en.word)
            )
