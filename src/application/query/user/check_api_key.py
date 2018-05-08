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

from src.domain.exception import ApiKeyDoesNotExist
from src.infrastructure.query_bus import QueryHandler


class CheckApiKeyQuery(object):
    """
    Checks if the API key of a developer exists
    """
    def __init__(self, api_key):
        self.api_key = api_key


class CheckApiKey(QueryHandler):
    def __init__(self):
        self.user_repository = None

    def invoke(self, query):
        user = self.user_repository.get_of_api_key(query.api_key)
        if not user:
            raise ApiKeyDoesNotExist
