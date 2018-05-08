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

from src.domain.model import Review
from src.domain.exception import RestaurantNotFoundInTwitter
from src.infrastructure.command_bus import CommandHandler


class RetrieveTwitterDataCommand(object):
    """
    Downloads Twitter data about a place and persist data in the repository
    """

    def __init__(self, place_name, geocode, project_id):
        """
        Creates a new command for retrieving Twitter data about a search

        :param place_name: Twitter search term -> #keyword, @person or plain
        :param geocode: [latitude, longitude, area]
        :param project_id: Project identifier
        """
        self.place_name = place_name
        self.geocode = geocode
        self.project_id = project_id


class RetrieveTwitterData(CommandHandler):
    def __init__(self):
        self.social_network_repository = None
        self.restaurant_repository = None
        self.review_repository = None
        self.twitter_client = None
        self.project_repository = None

    def invoke(self, command):
        tweets = self.__retrieve_tweets(command.place_name, command.geocode)
        project = self.__retrieve_project(command.project_id)
        self.__persist_tweets(command.place_name, tweets, project)

    def __retrieve_project(self, project_id):
        return self.project_repository.get_of_id(project_id)

    def __retrieve_tweets(self, place_name, geocode):
        return self.twitter_client.search_tweets_by_keyword(
            place_name, geocode
        )

    def __persist_tweets(self, place_name, tweets_content, project):
        twitter = self.social_network_repository.get_of_name('Twitter')
        restaurant = twitter.get_restaurant_of_id(place_name)
        if restaurant is None:
            raise RestaurantNotFoundInTwitter()
        restaurant.identifier = place_name
        restaurant.name = place_name
        twitter.add_restaurant(restaurant)
        self.social_network_repository.persist(twitter)
        self.__process_reviews(tweets_content, restaurant)
        project.add_restaurant(restaurant)
        self.project_repository.persist(project)

    def __process_reviews(self, tweets_content, restaurant):
        for tweet in tweets_content:
            if not self.__check_review_exists(restaurant, tweet['id']):
                review = Review(
                    item_reviewed=restaurant,
                    review_body=tweet['text'],
                    identifier=tweet['id']
                )
                self.review_repository.persist(review)
                restaurant.add_review(review)
        self.restaurant_repository.persist(restaurant)

    @staticmethod
    def __check_review_exists(restaurant, review_id):
        review = restaurant.get_review_of_id(review_id)
        return review is not None
