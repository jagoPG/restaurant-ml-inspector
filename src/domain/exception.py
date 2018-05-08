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


class AnalysisAlreadyCreatedException(Exception):
    """
    An analysis has been already created
    """


class AnalysisDoesNotExistException(Exception):
    """
    An analysis has not been created yet
    """


class KeywordAlreadyCreatedException(Exception):
    """
    A keyword has been already created
    """


class ProjectDoesNotExist(Exception):
    """
    Project does not exist
    """


class KeywordSynonymNoRegistered(Exception):
    """
    A keyword has no synonym group
    """


class SocialNetworkRestaurantDoesNotExist(Exception):
    """
    Social Network Restaurant instance does not exist
    """


class RestaurantNotFoundInFacebook(Exception):
    """
    Information about the restaurant not found in Facebook
    """


class RestaurantNotFoundInGooglePlaces(Exception):
    """
    Information about the restaurant not found at Google Places
    """


class RestaurantNotFoundInTwitter(Exception):
    """
    Information about the restaurant not found at Twitter
    """


class RestaurantAlreadyExists(Exception):
    """
    An instance of the restaurant already exists
    """


class ReviewIsNotAnalysable(Exception):
    """
    A review cannot be analysed
    """


class UserAlreadyExists(Exception):
    """
    User already exists
    """


class UserDoesNotExist(Exception):
    """
    User does not exist
    """


class RoleDoesNotExist(Exception):
    """
    User role does not exist
    """


class RoleAlreadyGranted(Exception):
    """
    The role has already been granted to the user
    """


class UserAccountNotActivated(Exception):
    """
    User account registered but not activated by the administrator.
    """


class AccessViolation(Exception):
    """
    User has no rights to perform an operation
    """


class ReviewDoesNotExist(Exception):
    """
    Review does not exist
    """


class ApiKeyDoesNotExist(Exception):
    """
    API key does not exist
    """
