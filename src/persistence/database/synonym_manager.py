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

from src.infrastructure.dependency_injector import Dependency
from xml.dom import minidom


class SynonymManager(Dependency):
    def __init__(self):
        self.file_path = None
        self.keyword_repository = None
        self._synonyms = {}

    def initialise(self):
        self.__read_synonym_list()

    def __read_synonym_list(self):
        xml_file = open(self.file_path, mode='r+', encoding='utf-8')
        document = minidom.parse(xml_file)
        for keyword in document.documentElement.getElementsByTagName('synonym'):
            identifier = keyword.getAttribute('identifier')
            values = []
            for value in keyword.getElementsByTagName('keyword'):
                values.append(value.firstChild.nodeValue)
            self._synonyms[identifier] = values
        xml_file.close()

    def get_synonym_group(self, synonym_id, language='en'):
        """
        Gets a group of synonym keywords
        :param synonym_id: The synonym group identifier
        :return: list of Keywords
        """
        keywords = []
        for word in self._synonyms[synonym_id]:
            keywords.append(
                self.keyword_repository.get_of_file_reference(word, language)
            )
        return keywords

    def get_synonym_group_identifier(self, keyword_id):
        for key, values in self._synonyms.items():
            if keyword_id in values:
                return key
        return None

