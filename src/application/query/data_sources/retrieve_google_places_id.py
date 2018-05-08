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
from src.domain.exception import RestaurantNotFoundInGooglePlaces


class RetrieveGooglePlacesIdQuery(object):
    """
    Gets data about a restaurant from Google Places
    """

    def __init__(self, place_name, country):
        self.place_name = place_name
        self.country = country


class RetrieveGooglePlacesId(QueryHandler):
    def __init__(self):
        self.google_client = None
        self.country_repository = None

    def invoke(self, query):
        country_name = self.__retrieve_country(query.country)
        return self.__search_and_filter_restaurant(
            query.place_name, country_name
        )

    def __retrieve_country(self, code):
        return self.country_repository.get_of_code(code).name

    def __search_and_filter_restaurant(self, restaurant_name, country):
        candidates = []
        response = self.google_client.search_place(restaurant_name)
        for restaurant in response['results']:
            if country.lower() in restaurant['formatted_address'].lower():
                candidates.append({
                    'id': restaurant['place_id'],
                    'name': restaurant['name'],
                    'address': RetrieveGooglePlacesId.__get_formatted_address(
                        restaurant['formatted_address']
                    )
                })
        if len(candidates) == 0:
            raise RestaurantNotFoundInGooglePlaces()
        return candidates

    @staticmethod
    def __get_formatted_address(address):
        if len(address) > 30:
            return '%s...' % address[:30]
        else:
            return address
