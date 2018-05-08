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

import logging
import requests
import json
from src.infrastructure.dependency_injector import Dependency


class FacebookClient(Dependency):
    """
    Provides easy access to Facebook API
    """

    OAUTH_URL = u'https://graph.facebook.com/oauth'
    API_URL = u'https://graph.facebook.com/v2.10'

    def __init__(self):
        self.app_id = None
        self.app_secret = None
        self.permissions = None
        self.access_token = None

    def initialise(self):
        self.access_token = self.generate_access_token()

    def generate_access_token(self):
        """
        Generates a temporal access token

        :return: Access Token as a JSON object
        """
        response = requests.get(
            FacebookClient.OAUTH_URL + u'/access_token', params={
                'client_id': self.app_id,
                'client_secret': self.app_secret,
                'grant_type': u'client_credentials'
            })
        if not response.ok:
            logging.error(response.content)
            raise FacebookException()
        response = json.loads(response.content)
        self.access_token = response['access_token']
        return self.access_token

    @staticmethod
    def retrieve_my_profile():
        """
        Retrieves the current's user information

        :return: Response as a JSON object
        """
        return requests.get(
            FacebookClient.API_URL + '/me/', params={
                'fields': u'id,name,picture',
                'access_token': u''
            }
        )

    def search_page(self, name):
        """
        Searches a page with a name

        :param name: Name of the page
        :return: List of pages that matches the query
        """
        response = requests.get(
            FacebookClient.API_URL + u'/search', params={
                'q': name,
                'type': u'page',
                'access_token': self.access_token
            }
        )
        if not response.ok:
            logging.error(response.content)
            raise FacebookException()
        return json.loads(response.content)

    def get_page_basic_information(self, page_id):
        """
        Gets the basic information available of a page

        :param page_id: identifier retrieved by :func:`search_page`
        :return: response as a JSON
        """
        response = requests.get(
            FacebookClient.API_URL + u'/%s' % page_id, params={
                'fields': u"""posts,events,about,birthday,category,
                 current_location,description,emails,food_styles,general_info,
                 hours,link,location,members,name,phone,username,website,
                 overall_star_rating,restaurant_services""",
                'access_token': self.access_token
            }
        )
        if not response.ok:
            logging.error(response.content)
            raise FacebookException()
        return json.loads(response.content)

    def get_page_feed(self, page_id, after=None):
        """
        Gets the public feed of a page with an identifier

        :param page_id: identifier retrieved by :func:`search_page`
        :param after: get the comments after an identifier returned by the previous request

        :return: response as a JSON
        """
        parameters = {
            'access_token': self.access_token,
            'limit': 30
        }
        if after is not None:
            parameters['after'] = after

        response = requests.get(
            FacebookClient.API_URL + u'/%s/feed/' % page_id,
            params=parameters
        )
        if not response.ok:
            logging.error(response.content)
            raise FacebookException()
        return json.loads(response.content)

    def get_page_tagged(self, page_id):
        response = requests.get(
            FacebookClient.API_URL + u'/%s/tagged/' % page_id, params={
                'access_token': self.access_token
            }
        )
        if not response.ok:
            logging.error(response.content)
            raise FacebookException()
        return json.loads(response.content)

    def get_visitor_posts(self, page_id):
        response = requests.get(
            FacebookClient.API_URL + u'/%s/visitor_posts' % page_id, params={
                'access_token': self.access_token
            }
        )
        if not response.ok:
            logging.error(response.content)
            raise FacebookException()
        return json.loads(response.content)

    @staticmethod
    def get_next_data_page(uri):
        """
        Gets the data from a pointer returned by a previous response
        :param uri: URI where the data is located
        :return: Response as a JSON object
        """
        response = requests.get(uri)
        if not response.ok:
            logging.error(response.content)
            raise FacebookException()
        return json.loads(response.content)


class FacebookException(Exception):
    """
    Facebook exception
    """
