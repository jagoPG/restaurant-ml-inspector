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

import twitter

from json import loads
from src.infrastructure.dependency_injector import Dependency
from urllib.parse import quote


class TwitterClient(Dependency):
    """
    Provides easy access to the Twitter API
    """

    def __init__(self):
        self.consumer_key = None
        self.consumer_secret = None
        self.access_token = None
        self.access_token_secret = None
        self.api = None

    def initialise(self):
        self.authenticate()

    def authenticate(self):
        """
        Authenticates for using the API

        :return: the API object
        """
        self.api = twitter.Api(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token_key=self.access_token,
            access_token_secret=self.access_token_secret
        )
        return self.api

    def get_user_details(self, username):
        """
        Gets user details

        :param username: Username
        :return: response as a JSON
        """
        response = self.api.UsersLookup(screen_name=username)

        return response

    def request_tweets_from_user(self, user_name, from_id=None):
        """
        Retrieves 200 tweets of the *user_name*. If *from_id* is specified gets
        the previous tweets

        :param user_name: Username
        :param from_id: Retrieve tweets older than the provided identifier
        :return: response as a JSON
        """
        if from_id is None:
            response = self.api.GetUserTimeline(
                screen_name=user_name,
                include_rts=False,
                exclude_replies=False,
                count=50
            )
        else:
            response = self.api.GetUserTimeline(
                screen_name=user_name,
                include_rts=False,
                exclude_replies=False,
                count=50,
                max_id=from_id
            )
        return self.transform_tweets(response)

    def search_tweets_by_keyword(self, keyword, geocode, since=None):
        """
        Retrieves tweets with a keyword

        :param keyword: keywords to be searched
        :param geocode: constrain the search to a location
        :param since: get tweets since a date

        :return: response as a JSON
        """
        query = u'q=%s&result_type=recent&count=50&lang=es' % quote(keyword)
        if since is not None:
            query += u'&since=%s' % '2014-1-1'
        if geocode is not None:
            query += u'&geocode=%s' % geocode
        response = self.api.GetSearch(
            raw_query=query
        )

        return self.transform_tweets(response)

    @staticmethod
    def transform_tweets(response):
        content = []
        for tweet in response:
            content.append(loads(tweet.__str__()))
        return content
