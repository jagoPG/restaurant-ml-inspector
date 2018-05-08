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

from src.domain.exception import KeywordAlreadyCreatedException
from src.domain.model import Keyword
from src.infrastructure.command_bus import CommandHandler


class CreateKeywordCommand(object):
    """
    Creates a new keyword in a certain language
    """
    def __init__(self, name, language):
        self.name = name
        self.language = language


class CreateKeyword(CommandHandler):
    def __init__(self):
        self.keyword_repository = None

    def invoke(self, command):
        self.__check_value_exists(command.name)
        self.__persist_keyword(command.name, command.language)

    def __check_value_exists(self, name):
        keyword = self.keyword_repository.get_of_name(name)
        if keyword is not None:
            raise KeywordAlreadyCreatedException

    def __persist_keyword(self, name, language):
        keyword = Keyword(
            word=name,
            language=language
        )
        self.keyword_repository.persist(keyword)
