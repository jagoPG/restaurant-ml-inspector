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


class GetCountriesQuery(object):
    """
    Gets all countries
    """


class GetCountries(QueryHandler):
    def __init__(self):
        self.country_repository = None
        self.country_data_transformer = None

    def invoke(self, query):
        countries = self.country_repository.all()
        plain_countries = list()
        for country in countries:
            self.country_data_transformer.write(country)
            plain_countries.append(self.country_data_transformer.read())
        return plain_countries
