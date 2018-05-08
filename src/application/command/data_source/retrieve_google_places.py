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
from src.infrastructure.command_bus import CommandHandler
from src.domain.exception import RestaurantNotFoundInGooglePlaces


class RetrieveGooglePlacesDataCommand(object):
    """
    Downloads data from GooglePlaces of a certain restaurant and persists the
    data
    """
    def __init__(self, project_id, restaurant_google_id):
        self.project_id = project_id
        self.restaurant_google_id = restaurant_google_id


class RetrieveGooglePlacesData(CommandHandler):
    def __init__(self):
        self.social_network_repository = None
        self.restaurant_repository = None
        self.review_repository = None
        self.google_client = None
        self.project_repository = None

    def invoke(self, command):
        detailed_response = self.google_client.retrieve_details(
            command.restaurant_google_id
        )
        project = self.__retrieve_project(command.project_id)
        self.__persist_restaurant(
            detailed_response, project, command.restaurant_google_id
        )

    def __retrieve_project(self, project_id):
        return self.project_repository.get_of_id(project_id)

    def __persist_restaurant(
            self, detailed_response, project, restaurant_network_id
    ):
        google_places = self.social_network_repository.get_of_name(
            'Google Places'
        )
        restaurant = self.__retrieve_restaurant_instance(
            restaurant_network_id, google_places, detailed_response
        )
        self.restaurant_repository.persist(restaurant)
        google_places.add_restaurant(restaurant)
        self.__process_reviews(detailed_response['reviews'], restaurant)
        project.add_restaurant(restaurant)

        self.social_network_repository.persist(google_places)
        self.project_repository.persist(project)
        self.restaurant_repository.persist(restaurant)

    def __retrieve_restaurant_instance(
            self, restaurant_network_id, google_places, response
    ):
        restaurant = google_places.get_restaurant_of_id(restaurant_network_id)
        if restaurant is None:
            raise RestaurantNotFoundInGooglePlaces()
        if 'opening_hours' in response:
            restaurant.opening_hours = self.__format_timetable(
                response['opening_hours']['weekday_text']
            )
        if 'formatted_address' in response:
            restaurant.address = response['formatted_address']
        if 'rating' in response:
            restaurant.star_rating = response['rating']
        if 'formatted_phone_number' in response:
            restaurant.telephone = response['formatted_phone_number']
        location = RetrieveGooglePlacesData.__retrieve_geo_location(response)
        restaurant.identifier = response['url']
        restaurant.social_network_identifier = response['place_id']
        restaurant.name = response['name']
        restaurant.geo = location
        return restaurant

    @staticmethod
    def __retrieve_geo_location(response):
        if 'geometry' not in response:
            return None
        location = response['geometry']
        if 'location' not in location:
            return None
        location = location['location']
        return '%s,%s' % (location['lat'], location['lng'])

    @staticmethod
    def __format_timetable(timetable):
        opening_hours = ''
        for day in timetable:
            opening_hours += '<p>%s</p>\n' % day
        return opening_hours

    def __process_reviews(self, reviews, restaurant):
        for review in reviews:
            if 'author_url' in review:
                review_id = review['author_url']
            else:
                review_id = review['time']
            if not self.__check_review_exists(restaurant, review_id):
                review = Review(
                    identifier=review_id,
                    item_reviewed=restaurant,
                    review_body=review['text']
                )
                self.review_repository.persist(review)
                restaurant.add_review(review)

    @staticmethod
    def __check_review_exists(restaurant, review_id):
        review = restaurant.get_review_of_id(review_id)
        return review is not None
