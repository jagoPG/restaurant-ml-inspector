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

from flask import current_app, json

from src.application.query.country.get_countries import GetCountriesQuery
from web.routing.actions.action import Action


class GetCountries(Action):
    def __init__(self):
        self.query_bus = None

    def invoke(self, request=None, **kwargs):
        response = self.query_bus.execute(GetCountriesQuery())
        return current_app.response_class(
            status=200, response=json.dumps(response)
        )
