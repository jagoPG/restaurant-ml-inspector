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

from src.application.analysis.evaluated_word import EvaluatedWord
from src.infrastructure.dependency_injector import Dependency


class WordListSynonymReducer(Dependency):
    """
    Converts several list of words into a single list which synonym words have
    been merged into one single list
    """
    def __init__(self):
        self.word_repository = None
        self.words = {}

    def clean(self):
        self.words = {}

    def reduce(self, word_list, language):
        word_list = [item for item in word_list.values()]
        are_synonyms = False
        i = 0
        while i < len(word_list):
            data = word_list[i]
            word = data.word
            j = 0

            stored_words = [item for item in self.words.values()]
            while j < len(stored_words):
                data_stored = stored_words[j]
                word_stored = data_stored.word
                are_synonyms = self.__are_word_synonyms(
                    word, word_stored, language, data_stored.language
                )
                if are_synonyms:
                    self.__select_dominant_word(data, data_stored, language)
                    break
                j += 1
            if not are_synonyms:
                data.language = language
                self.words[word] = data
            i += 1
        return self.words

    def __are_word_synonyms(self, word_a, word_b, language_a, language_b):
        word_a = self.word_repository.get_of_name(word_a, language_a)
        word_b = self.word_repository.get_of_name(word_b, language_b)
        if not word_a or not word_b:
            return False
        return word_a.are_synonyms(word_b) \
               or word_b.are_synonyms(word_a) \
               or word_a.are_translations(word_b) \
               or word_b.are_translations(word_a)

    def __select_dominant_word(
            self, current_word_data, stored_word_data, current_word_language
    ):
        """
        Compares two words data that are synonyms for selecting the one which
        had more appearances in the reviews.
        
        :param current_word_data: EvaluatedWord instance of current word
        :param stored_word_data: EvaluatedWord instance of categorized word
        :param current_word_language: Language of current word data
        """
        karma = (current_word_data.karma + stored_word_data.karma) / 2
        appearances = \
            current_word_data.appearances + stored_word_data.appearances
        if current_word_data.count > stored_word_data.count:
            word = current_word_data.word
            self.words[word] = EvaluatedWord(
                word, karma, appearances
            )
            self.words[word].language = current_word_language
            del self.words[stored_word_data.word]
        else:
            word = stored_word_data.word
            self.words[word].appearances = appearances
            self.words[word].karma = karma
            self.words[word].count = len(appearances)
