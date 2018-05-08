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

from datetime import datetime
from neomodel import cardinality
from src.domain.exception import AnalysisDoesNotExistException
from src.domain.model import AnalysisRestaurant
from src.infrastructure.command_bus import CommandHandler
from re import compile


class ProcessRestaurantOverviewCommand(object):
    """
    Processes the restaurant's stored social network basic data (contact data,
    timetables, description...) and creates just one instance with all the
    information.

    In order to decide which data is chosen, the length of the
    fields is compared and the longer one is which is stored in the analysis
    entity.
    """

    def __init__(self, project_id, analysis_id):
        self.project_id = project_id
        self.analysis_id = analysis_id
        self.requested_on = datetime.now()


class ProcessRestaurantOverview(CommandHandler):
    TELEPHONE_REGEX = '(\+\d{3}){0,1}(\d{9})'

    # @author Iain Fraser
    GEOPOSITION_REGEX = '^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'

    def __init__(self):
        self.project_repository = None
        self.analysis_repository = None
        self._telephone_validator = compile(
            ProcessRestaurantOverview.TELEPHONE_REGEX)
        self._geoposition_validator = compile(
            ProcessRestaurantOverview.GEOPOSITION_REGEX)
        self._restaurant_names = []
        self._restaurant_address = []

    def invoke(self, command):
        project = self.__retrieve_project(command.project_id)
        self.__check_analysis_is_created(project)
        restaurants = self.__retrieve_restaurants_data(project)
        self.__process_overview_data(restaurants, project.analysis.single())

    def __retrieve_project(self, identifier):
        return self.project_repository.get_of_id(identifier)

    @staticmethod
    def __check_analysis_is_created(project):
        if project.analysis is None:
            raise AnalysisDoesNotExistException()

    @staticmethod
    def __retrieve_restaurants_data(project):
        return project.restaurants.all()

    def __process_overview_data(self, restaurants, analysis):
        try:
            analysis_restaurant = analysis.restaurant.single()
        except cardinality.CardinalityViolation:
            analysis_restaurant = self.__create_analysis_restaurant_instance(
                analysis)
        for restaurant in restaurants:
            self.__mix_social_network_data(restaurant, analysis_restaurant)
        self.__store_valid_restaurant_name(analysis_restaurant)
        self.__store_valid_restaurant_address(analysis_restaurant)
        analysis_restaurant.save()

    def __create_analysis_restaurant_instance(self, analysis):
        analysis_restaurant = AnalysisRestaurant(
            analysis=analysis
        )
        analysis_restaurant.save()
        analysis.add_restaurant(analysis_restaurant)
        self.analysis_repository.persist(analysis)
        return analysis_restaurant

    def __mix_social_network_data(self, restaurant, analysis_restaurant):
        if restaurant.name is not None:
            self._restaurant_names.append(restaurant.name)
        if restaurant.address is not None:
            self._restaurant_address.append(restaurant.address)

        if self.__has_to_be_mixed_string_field(
                analysis_restaurant.opening_hours, restaurant.opening_hours):
            analysis_restaurant.opening_hours = restaurant.opening_hours
        if self.__has_to_be_mixed_string_field(
                analysis_restaurant.description, restaurant.description
        ):
            analysis_restaurant.description = restaurant.description
        if self.__is_valid_telephone_number(restaurant.telephone):
            analysis_restaurant.telephone = restaurant.telephone
        if self.__is_valid_geocoordinates(restaurant.geo):
            analysis_restaurant.geo = restaurant.geo
        if restaurant.accepts_reservations:
            analysis_restaurant.accepts_reservations = True
        ProcessRestaurantOverview.__calculate_rating_average(
            restaurant, analysis_restaurant
        )

    @staticmethod
    def __calculate_rating_average(restaurant, analysis_restaurant):
        if not restaurant.star_rating:
            return
        if analysis_restaurant.star_rating is None:
            average = restaurant.star_rating
        else:
            average = (
                              analysis_restaurant.star_rating + restaurant.star_rating) / 2
        analysis_restaurant.star_rating = round(float(average))

    def __is_valid_telephone_number(self, phone_number):
        if phone_number is None:
            return False
        phone_number = ''.join(
            [char for char in phone_number if char not in ['.', '-', ' ']])
        return self._telephone_validator.match(phone_number) is not None

    def __is_valid_geocoordinates(self, geo):
        if geo is None:
            return False
        geo = geo.replace(' ', '')
        return self._geoposition_validator.match(geo) is not None

    @staticmethod
    def __has_to_be_mixed_string_field(current, candidate):
        if candidate is not None and (
                current is None or len(current) < len(candidate)):
            return True
        return False

    def __store_valid_restaurant_name(self, restaurant):
        tokenized_names = self.__tokenize_array(self._restaurant_names)
        candidate_index = self.__select_candidate(tokenized_names)
        if len(self._restaurant_names) > 0:
            restaurant.name = self._restaurant_names[candidate_index]

    def __store_valid_restaurant_address(self, restaurant):
        tokenized_names = self.__tokenize_array(self._restaurant_address)
        candidate_index = self.__select_candidate(tokenized_names)
        if len(self._restaurant_address) > 0:
            restaurant.address = self._restaurant_address[candidate_index]

    @staticmethod
    def __tokenize_name(name):
        name = ''.join(
            [char for char in name if char not in [',', '.', 'º', 'ª']])
        name_tokens = name.split(' ')
        return name_tokens

    @staticmethod
    def __tokenize_array(items):
        tokenized_names = []
        for name in items:
            tokenized_names.append(
                ProcessRestaurantOverview.__tokenize_name(name)
            )
        return tokenized_names

    @staticmethod
    def __select_candidate(tokenized_names):
        # For each phrase calculate the amount of words that match
        matches = []
        matches.extend(0 for item in tokenized_names)
        item_a = 0
        items = len(tokenized_names)
        while item_a < items:
            item_b = item_a + 1
            while item_b < items:
                matches[
                    item_a] += ProcessRestaurantOverview.__count_same_words(
                    tokenized_names[item_a], tokenized_names[item_b]
                )
                item_b += 1
            item_a += 1

        # Select the phrase with greatest matches
        greatest_match = -1
        index = 0
        while index < items - 1:
            if matches[index] > matches[index + 1]:
                greatest_match = index
            else:
                greatest_match = index + 1
            index += 1
        return greatest_match

    @staticmethod
    def __count_same_words(phrase_a, phrase_b):
        word_match = 0
        for item_a in phrase_a:
            for item_b in phrase_b:
                if item_a == item_b:
                    word_match += 1
        return word_match
