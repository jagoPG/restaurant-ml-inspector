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

from src.domain.exception import UserDoesNotExist, UserAccountNotActivated
from src.infrastructure.query_bus import QueryHandler
from datetime import datetime


class GetUserQuery(object):
    """
    Gets an user
    """
    def __init__(self, user_id):
        self.user_id = user_id


class GetUser(QueryHandler):
    def __init__(self):
        self.user_repository = None
        self.user_data_transformer = None

    def invoke(self, query):
        user = self.__get_user(query.user_id)
        self.__check_user_access(user)
        self.__modify_access_date(user)
        self.user_data_transformer.write(user)
        return self.user_data_transformer.read()

    def __get_user(self, user_id):
        user = self.user_repository.get_of_identifier(user_id)
        if not user:
            raise UserDoesNotExist()
        return user

    @staticmethod
    def __check_user_access(user):
        if not user.is_verified:
            raise UserAccountNotActivated()

    def __modify_access_date(self, user):
        user.last_login = datetime.now()
        self.user_repository.persist(user)
