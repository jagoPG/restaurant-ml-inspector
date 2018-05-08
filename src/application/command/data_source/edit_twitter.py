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
from src.domain.exception import RestaurantNotFoundInTwitter


class EditTwitterSourceCommand(object):
    """
    Modifies a restaurant source from Twitter
    """
    def __init__(self, project_id, name, geo_position):
        self.project_id = project_id
        self.name = name
        self.geo_position = geo_position


class EditTwitterSource(CommandHandler):
    def __init__(self):
        self.project_repository = None
        self.social_network_repository = None
        self.restaurant_repository = None

    def invoke(self, command):
        project = self.__retrieve_project(command.project_id)
        twitter = self.__retrieve_social_network()
        restaurant = self.__retrieve_restaurant(project, twitter)
        self.__edit_restaurant_instance(restaurant, command)
        self.__remove_reviews(restaurant)

    def __retrieve_project(self, project_id):
        return self.project_repository.get_of_id(project_id)

    def __retrieve_social_network(self):
        return self.social_network_repository.get_of_name('Twitter')

    @staticmethod
    def __retrieve_restaurant(project, social_network):
        restaurants = project.get_restaurants()
        for restaurant in restaurants:
            if social_network.has_restaurant(restaurant):
                return restaurant
        raise RestaurantNotFoundInTwitter()

    def __remove_reviews(self, restaurant):
        self.restaurant_repository.remove_reviews(restaurant)

    def __edit_restaurant_instance(self, restaurant, command):
        restaurant.social_network_identifier = command.name
        restaurant.identifier = command.name
        restaurant.geo = command.geo_position
        self.restaurant_repository.persist(restaurant)
