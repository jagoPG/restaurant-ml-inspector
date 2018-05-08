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
from src.domain.exception import RestaurantAlreadyExists
from src.domain.model import SocialNetworkRestaurant


class AddGooglePlacesSourceCommand(object):
    """
    Adds a new restaurant source from Google Places
    """
    def __init__(self, project_id, name, country):
        self.project_id = project_id
        self.name = name
        self.country = country


class AddGooglePlacesSource(CommandHandler):
    def __init__(self):
        self.project_repository = None
        self.social_network_repository = None
        self.country_repository = None
        self.restaurant_repository = None

    def invoke(self, command):
        project = self.__retrieve_project(command.project_id)
        google_places = self.__retrieve_social_network()
        self.__check_restaurant_not_exists(project, google_places)
        country = self.__retrieve_country(command.country)
        self.__create_restaurant_instance(
            command, project, country, google_places
        )

    def __retrieve_project(self, project_id):
        return self.project_repository.get_of_id(project_id)

    def __retrieve_social_network(self):
        return self.social_network_repository.get_of_name('Google Places')

    @staticmethod
    def __check_restaurant_not_exists(project, social_network):
        restaurants = project.get_restaurants()
        for restaurant in restaurants:
            if social_network.has_restaurant(restaurant):
                raise RestaurantAlreadyExists()

    def __retrieve_country(self, country):
        return self.country_repository.get_of_code(country)

    def __create_restaurant_instance(
            self, command, project, country, social_network
    ):
        restaurant = SocialNetworkRestaurant(
            social_network_identifier=command.name,
            country=country,
            project=project
        )
        self.restaurant_repository.persist(restaurant)
        project.add_restaurant(restaurant)
        social_network.add_restaurant(restaurant)
        country.add_restaurant(restaurant)
        self.country_repository.persist(country)
        self.project_repository.persist(project)
        self.social_network_repository.persist(social_network)
