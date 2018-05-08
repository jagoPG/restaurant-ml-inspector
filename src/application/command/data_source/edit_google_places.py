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

from src.infrastructure.command_bus import CommandHandler
from src.domain.exception import RestaurantNotFoundInGooglePlaces


class EditGooglePlacesSourceCommand(object):
    """
    Modifies a restaurant source from Google places
    """
    def __init__(self, project_id, name, country):
        self.project_id = project_id
        self.name = name
        self.country = country


class EditGooglePlacesSource(CommandHandler):
    def __init__(self):
        self.project_repository = None
        self.social_network_repository = None
        self.country_repository = None
        self.restaurant_repository = None

    def invoke(self, command):
        project = self.__retrieve_project(command.project_id)
        google_client = self.__retrieve_social_network()
        restaurant = self.__retrieve_restaurant(project, google_client)

        if command.name == '':
            google_client.remove_restaurant(restaurant)
            self.restaurant_repository.remove(restaurant)
        else:
            country = self.__retrieve_country(command.country)
            self.__edit_restaurant_instance(restaurant, command, country)

    def __retrieve_project(self, project_id):
        return self.project_repository.get_of_id(project_id)

    def __retrieve_social_network(self):
        return self.social_network_repository.get_of_name('Google Places')

    @staticmethod
    def __retrieve_restaurant(project, social_network):
        restaurants = project.get_restaurants()
        for restaurant in restaurants:
            if social_network.has_restaurant(restaurant):
                return restaurant
        raise RestaurantNotFoundInGooglePlaces()

    def __retrieve_country(self, country):
        return self.country_repository.get_of_code(country)

    def __edit_restaurant_instance(self, restaurant, command, country):
        if len(restaurant.country) > 0:
            restaurant.get_country().remove_restaurant(restaurant)
        restaurant.social_network_identifier = command.name
        restaurant.country = country
        self.__clean_data(restaurant)
        self.restaurant_repository.persist(restaurant)
        country.add_restaurant(restaurant)
        self.country_repository.persist(country)

    @staticmethod
    def __clean_data(restaurant):
        restaurant.name = ''
        restaurant.accepts_reservation = False
        restaurant.star_rating = 0
        restaurant.opening_hours = ''
        restaurant.telephone = ''
        restaurant.description = ''
        restaurant.geo = ''
