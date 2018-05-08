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
from src.domain.exception import SocialNetworkRestaurantDoesNotExist


class EditProjectSocialNetworkDataCommand(object):
    """
    Removes the reviews related with the SocialNetworkRestaurant and changes
    the social network identifier of the instance.
    """

    def __init__(
            self, sn_restaurant_id, new_restaurant_name
    ):
        """
        Command DTO
        :param sn_restaurant_id: The social network identifier of the
        SocialNetworkRestaurant entity
        :param new_restaurant_name: The new identifier of the restaurant in
        the social network
        """
        self.social_network_restaurant_identifier = sn_restaurant_id
        self.new_restaurant_name = new_restaurant_name


class EditProjectSocialNetworkData(CommandHandler):
    def __init__(self):
        self.restaurant_social_network = None

    def invoke(self, command):
        restaurant = self.__retrieve_restaurant(command.sn_restaurant_id)
        self.__remove_reviews(restaurant)
        self.__edit_restaurant_name(restaurant, command.new_restaurant_name)

    def __retrieve_restaurant(self, restaurant_id):
        restaurant = self.restaurant_social_network.get_of_id(restaurant_id)
        if restaurant is None:
            raise SocialNetworkRestaurantDoesNotExist()
        return restaurant

    def __remove_reviews(self, restaurant):
        self.restaurant_social_network.remove_reviews(restaurant)

    def __edit_restaurant_name(self, restaurant, name_of_restaurant):
        restaurant.social_network_identifier = name_of_restaurant
        self.restaurant_social_network.persist(restaurant)
