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
from src.domain.exception import RestaurantNotFoundInFacebook


class RetrieveFacebookIdQuery(object):
    """
    Gets a Facebook page with an identifier from the social network
    """

    def __init__(self, restaurant_name, country):
        self.restaurant_name = restaurant_name
        self.country = country


class RetrieveFacebookId(QueryHandler):
    def __init__(self):
        self.facebook_client = None
        self.country_repository = None

    def invoke(self, query):
        country = self.__retrieve_country(query.country)
        return self.__search_and_filter_restaurant(
            query.restaurant_name, country
        )

    def __retrieve_country(self, code):
        return self.country_repository.get_of_code(code).name

    def __search_and_filter_restaurant(self, restaurant_name, country):
        response = self.facebook_client.search_page(restaurant_name)
        restaurants = self.__filter_by_country(country, response)
        if len(restaurants) == 0:
            raise RestaurantNotFoundInFacebook()
        else:
            return restaurants

    def __filter_by_country(self, country, response):
        """
        One dictionary stores all detailed places, if there is one or more
        places after the filter is applied the cache is replaced by the
        filtered places
        """
        restaurants = list()
        for candidate in response['data']:
            detailed_response = self.facebook_client.get_page_basic_information(
                candidate['id']
            )
            if 'location' in detailed_response and \
                    'country' in detailed_response['location']:
                response_country = detailed_response['location']['country']
                if response_country.lower() == country.lower():
                    restaurants.append({
                        'id': candidate['id'],
                        'name': candidate['name'],
                        'address': RetrieveFacebookId.__generate_address(
                            detailed_response['location']
                        )
                    })
        return restaurants

    @staticmethod
    def __generate_address(location):
        address = ''
        if 'street' in location:
            address += location['street']
        if 'city' in location:
            address += ', ' + location['city']
        if 'zip' in location:
            address += ', ' + location['zip']
        return address
