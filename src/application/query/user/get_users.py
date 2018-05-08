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

from src.infrastructure.query_bus import QueryHandler


class GetUsersQuery(object):
    """
    Gets users
    """


class GetUsers(QueryHandler):
    def __init__(self):
        self.user_repository = None
        self.user_data_transformer = None

    def invoke(self, query):
        dto_users = []
        users = self.user_repository.all()
        for user in users:
            self.user_data_transformer.write(user)
            dto_users.append(
                self.user_data_transformer.read()
            )
        return dto_users
