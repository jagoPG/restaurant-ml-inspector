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

from flask import request, Blueprint
from web.routing.actions.action import execute_action
from web.routing.decorator.decorators import is_xhr, are_args_in_query, \
    has_valid_api_key

MAX_DISTANCE = 1
api_page = Blueprint('api', __name__, template_folder='templates')


@api_page.route('/project/restaurant/<project_id>/', methods=['GET'])
@is_xhr
def get_restaurant_details(project_id):
    return execute_action(
        'app.action.api.get_restaurant_details', None, project_id=project_id
    )


@api_page.route('/projects/', methods=['GET'])
def get_available_projects():
    return execute_action('app.action.api.get_available_projects')


@api_page.route('/project/<project_id>/', methods=['GET'])
def get_project_basic_data(project_id):
    return execute_action(
        'app.action.api.get_project_basic_data', None, project_id=project_id
    )


@api_page.route('/project/details/<project_id>/', methods=['GET'])
def get_project_details(project_id):
    return execute_action(
        'app.action.api.get_project_details', None, project_id=project_id
    )


@api_page.route('/project/sources/<project_id>/', methods=['GET'])
def get_project_data_sources(project_id):
    return execute_action(
        'app.action.api.get_project_data_sources', None, project_id=project_id
    )


@api_page.route('/sources/', methods=['GET'])
@is_xhr
@are_args_in_query(query_args=('country', 'name', 'network'))
def get_restaurant_network_identifier():
    """
    Retrieves the identifier of a restaurant in the social network passed in the
    query parameter. The restaurant name has to be passed as query parameter.
    e.g.:
        /admin/project/sources/?name=example&network=(Google%20Places|Facebook)
    :return: The identifier of the restaurant as a JSON object
    """
    return execute_action(
        'app.action.api.get_restaurant_network_identifier', request
    )


@api_page.route('/country/', methods=['GET'])
@is_xhr
def get_countries():
    return execute_action('app.action.api.get_countries')


@api_page.route('/restaurant/nearby/', methods=['GET'])
@is_xhr
@are_args_in_query(query_args=('latitude', 'longitude'))
def get_nearby_restaurants():
    return execute_action('app.action.api.get_nearby_restaurants', request)


@api_page.route('/project/retrieve-data/<project_id>/', methods=['PUT'])
@has_valid_api_key
def request_retrieve_data_from_social_networks(project_id):
    return execute_action(
        'app.action.request_retrieve_data_from_social_networks',
        None,
        project_id=project_id
    )


@api_page.route('/project/analyse/<project_id>/', methods=['PUT'])
@has_valid_api_key
def request_analysis(project_id):
    return execute_action(
        'app.action.request_analysis', None, project_id=project_id
    )
