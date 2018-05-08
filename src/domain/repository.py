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


class SocialNetworkRepository(object):
    """
    Social Network Repository
    """

    def persist(self, instance):
        """
        Persist instance
        """
        raise NotImplementedError()

    def remove(self, instance):
        """
        Remove an instance
        """
        raise NotImplementedError()

    def get_of_name(self, name):
        """
        Get an instance of social network with a name
        """
        raise NotImplementedError()


class RestaurantRepository(object):
    """
    Restaurant Repository
    """

    def persist(self, instance):
        """
        Persist instance
        """

    def remove(self, restaurant):
        """
        Remove an instance
        """
        raise NotImplementedError()

    def get_of_name(self, social_network, name):
        """
        Get an instance of social network with a name
        """
        raise NotImplementedError()

    def all(self):
        """
        Retrieves all Analysis Restaurants
        """


class ReviewRepository(object):
    """
    Review Repository
    """

    def persist(self, instance):
        """
        Persist instance
        """

    def remove(self, review):
        """
        Remove an instance
        """
        raise NotImplementedError()

    def get_of_id(self, identifier):
        """
        Get review with an identifier
        """

    def get_scored_reviews(self):
        """
        Get user scored _reviews
        """


class ProjectRepository(object):
    """
    Project Repository
    """

    def all(self):
        """
        Retrieves all projects
        """
        raise NotImplementedError()

    def persist(self, instance):
        """
        Persist instance
        """
        raise NotImplementedError()

    def remove(self, instance):
        """
        Remove an instance
        """
        raise NotImplementedError()

    def get_of_name(self, name):
        """
        Get an instance of project with a name
        """
        raise NotImplementedError()

    def get_of_id(self, identifier):
        """
        Get an instance of project with an ID
        """
        raise NotImplementedError()


class AnalysisRepository(object):
    """
    Analysis Repository
    """

    def persist(self, instance):
        """
        Persist instance
        """

    def remove(self, instance):
        """
        Remove an instance
        """
        raise NotImplementedError()

    def get_of_id(self, identifier):
        """
        Get an instance of project with an identifier
        """
        raise NotImplementedError()


class KeyPointRepository(object):
    """
    Key Point Repository
    """

    def persist(self, instance):
        """
        Persist instance
        """
        raise NotImplementedError()

    def remove(self, instance):
        """
        Remove an instance
        """
        raise NotImplementedError()


class CountryRepository(object):
    """
    Country repository
    """

    def persist(self, country):
        """
        Create a new country
        """
        raise NotImplementedError

    def all(self):
        """
        Retrieves all countries
        """
        raise NotImplementedError

    def get_of_code(self, code):
        """
        Gets a country with a code
        """
        raise NotImplementedError


class KeywordRepository(object):
    """
    Key word repository
    """

    def persist(self, keyword):
        """
        Persist instance
        """
        raise NotImplementedError()

    def remove(self, keyword):
        """
        Remove instance
        """
        raise NotImplementedError()

    def get_of_name(self, name, language):
        """
        Gets keyword with name
        """
        raise NotImplementedError()

    def get_word_like(self, name, language):
        """
        Gets keyword similar to the name
        """
        raise NotImplementedError()

    def get_all(self):
        """
        Gets all keywords
        """
        raise NotImplementedError()

    def get_of_file_reference(self, file_reference, language):
        """
        Gets a keyword with reference and name
        """
        raise NotImplementedError()


class UserRepository(object):
    def persist(self, user):
        """
        Persists user instance
        """
        raise NotImplementedError()

    def remove(self, user):
        """
        Removes user instance
        """
        raise NotImplementedError()

    def all(self):
        """
        Retrieves all users
        """
        raise NotImplementedError()

    def activate_user(self, user):
        """
        Activates an user
        """
        raise NotImplementedError()

    def deactivate_user(self, user):
        """
        Blocks an user's access
        """
        raise NotImplementedError()

    def get_of_identifier(self, identifier):
        """
        Gets an user with an identifier
        """
        raise NotImplementedError()

    def get_of_api_key(self, api_key):
        """
        Gets an user with an API key
        """
        raise NotImplementedError
