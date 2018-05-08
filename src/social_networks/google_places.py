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

import requests
from json import loads

from src.infrastructure.dependency_injector import Dependency


class GooglePlacesClient(Dependency):
    """
    Provides easy access to Google Places API
    """

    TEXT_SEARCH_API_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
    DETAILS_API_URL = 'https://maps.googleapis.com/maps/api/place/details/json?'

    def __init__(self):
        self.api_key = None

    def search_place(self, name):
        """
        Searches a place with a name

        :param name: Name of the place
        :return: request response as a JSON object
        """
        url = GooglePlacesClient.TEXT_SEARCH_API_URL + 'query=' + name + '&key=' + self.api_key
        response = requests.get(url)
        return loads(response.content)

    def retrieve_details(self, place_id):
        """
        Retrieves the details of a place

        :param place_id: The place ID retrieved by :func:`search_place`
        :return: request response as a JSON object
        """
        url = GooglePlacesClient.DETAILS_API_URL + 'placeid=' + place_id + \
              '&key=' + self.api_key
        response = requests.get(url)
        return loads(response.content)['result']
