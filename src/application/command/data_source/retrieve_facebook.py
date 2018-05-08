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
from src.domain.exception import RestaurantNotFoundInFacebook


class RetrieveFacebookDataCommand(object):
    """
    Retrieves Facebook of a page and stores in the repository
    """

    def __init__(self, project_id, facebook_page_id):
        self.project_id = project_id
        self.facebook_page_id = facebook_page_id


class RetrieveFacebookData(CommandHandler):
    WEEK_DAYS = {
        'mon': 'Monday', 'tue': 'Tuesday', 'wed': 'Wednesday',
        'thu': 'Thursday', 'fri': 'Friday', 'sat': 'Saturday',
        'sun': 'Sunday'
    }

    def __init__(self):
        self.social_network_repository = None
        self.restaurant_repository = None
        self.review_repository = None
        self.facebook_client = None
        self.project_repository = None

    def invoke(self, command):
        response = self.__retrieve_page_details(command.facebook_page_id)
        if response is not None:
            project = self.__retrieve_project(command.project_id)
            self.__persist_restaurant(
                response, project, command.facebook_page_id
            )

    def __retrieve_project(self, project_id):
        return self.project_repository.get_of_id(project_id)

    def __retrieve_page_details(self, facebook_page_id):
        return self.facebook_client.get_page_basic_information(
            facebook_page_id
        )

    def __persist_restaurant(self, response, project, restaurant_network_id):
        facebook = self.social_network_repository.get_of_name('Facebook')
        restaurant = self.__retrieve_restaurant_instance(
            restaurant_network_id,
            facebook,
            response
        )
        self.__set_restaurant_data(restaurant, response)
        self.restaurant_repository.persist(restaurant)
        facebook.add_restaurant(restaurant)
        self.social_network_repository.persist(facebook)

        self.__process_reviews(response['id'], restaurant)
        self.restaurant_repository.persist(restaurant)

        project.add_restaurant(restaurant)
        self.project_repository.persist(restaurant)

    @staticmethod
    def __retrieve_restaurant_instance(
            restaurant_network_id, facebook, response
    ):
        restaurant = facebook.get_restaurant_of_id(restaurant_network_id)
        if restaurant is None:
            raise RestaurantNotFoundInFacebook()
        restaurant.identifier = response['link']
        restaurant.name = response['name']
        return restaurant

    def __set_restaurant_data(self, restaurant, response):
        RetrieveFacebookData.__add_restaurant_description(restaurant, response)
        if 'phone' in response:
            restaurant.telephone = response['phone']
        if 'location' in response:
            restaurant.address, restaurant.geo = self.__generate_address(
                response['location']
            )
        if 'hours' in response:
            restaurant.opening_hours = self.__process_timetable(
                response['hours']
            )
        if 'overall_star_rating' in response:
            restaurant.star_rating = response['overall_star_rating']

    @staticmethod
    def __add_restaurant_description(restaurant, response):
        description = ''
        if 'about' in response:
            description += response['about'].capitalize()
        if 'description' in response:
            description += response['description'].capitalize()
        restaurant.description = description

    @staticmethod
    def __generate_address(location):
        address = ''
        geo = None
        if 'street' in location:
            address += location['street']
        if 'city' in location:
            address += ', ' + location['city']
        if 'zip' in location:
            address += ', ' + location['zip']
        if 'country' in location:
            address += ', ' + location['country']
        if 'latitude' in location and 'longitude' in location:
            geo = '%s,%s' % (location['latitude'], location['longitude'])
        return address, geo

    @staticmethod
    def __process_timetable(timetable):
        parsed_timetable = ''
        for shortening, day in RetrieveFacebookData.WEEK_DAYS.items():
            open_key = shortening + '_1_open'
            if open_key not in timetable:
                parsed_timetable += day + ': CLOSED\n'
                continue
            close_key = shortening + '_1_close'
            parsed_timetable += '<p>%s: %s-%s</p>\n' % (
                day, timetable[open_key], timetable[close_key]
            )

        return parsed_timetable

    def __process_reviews(self, page_id, restaurant):
        # Process initial page
        response = self.facebook_client.get_visitor_posts(page_id)
        self.__save_reviews(response, restaurant)

        # Iterate through reviews pages
        while 'paging' in response and 'next' in response['paging']:
            response = self.facebook_client.get_next_data_page(
                response['paging']['next']
            )
            self.__save_reviews(response, restaurant)

    def __save_reviews(self, feed_response, restaurant):
        for review in feed_response['data']:
            if 'message' not in review:
                continue
            if not self.__check_review_exists(restaurant, review['id']):
                persist_review = Review(
                    identifier=review['id'],
                    review_body=review['message'],
                    item_reviewed=restaurant
                )
                self.review_repository.persist(persist_review)
                restaurant.add_review(persist_review)

    @staticmethod
    def __check_review_exists(restaurant, review_id):
        review = restaurant.get_review_of_id(review_id)
        return review is not None
