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

from flask import Blueprint, current_app as app
from web.routing.actions.action import execute_action
from web.routing.decorator.decorators import is_xhr, is_admin, \
    has_permission_to_project, are_args_in_json_request, is_logged

admin_page = Blueprint('admin', __name__, template_folder='templates')


@admin_page.route('/', methods=['GET'])
def get_admin():
    return execute_action('app.action.admin.get_admin')


@admin_page.route('/user/activate/<user_id>/', methods=['PUT'])
@is_xhr
@is_admin
def activate_user(user_id):
    return execute_action('app.action.admin.activate_user', None, user_id=user_id)


@admin_page.route('/user/roles/<user_id>/', methods=['PUT'])
@is_xhr
@is_admin
@are_args_in_json_request(json_args=('roles',))
def grant_user_role(user_id, json_data):
    return execute_action(
        'app.action.admin.grant_user_role', None, user_id=user_id, json_data=json_data
    )


@admin_page.route('/user/deactivate/<user_id>/', methods=['PUT'])
@is_xhr
@is_admin
def disable_user(user_id):
    return execute_action(
        'app.action.admin.disable_user', None, user_id=user_id
    )


@admin_page.route('/users/', methods=['GET'])
@is_xhr
@is_admin
def get_users():
    return execute_action('app.action.admin.get_users')


@admin_page.route('/project/', methods=['POST'])
@is_xhr
@is_logged
@are_args_in_json_request(json_args=('name', 'description'))
def create_project(json_data):
    return execute_action(
        'app.action.admin.create_project', None, json_data=json_data
    )


@admin_page.route('/projects/', methods=['GET'])
@is_xhr
@is_logged
def get_projects():
    return execute_action('app.action.admin.get_projects')


@admin_page.route('/project/<project_id>/', methods=['PUT'])
@is_xhr
@is_logged
@has_permission_to_project
@are_args_in_json_request(json_args=('name', 'description'))
def edit_project(project_id, json_data):
    return execute_action(
        'app.action.admin.edit_project', None, project_id=project_id,
        json_data=json_data
    )


@admin_page.route('/project/<project_id>/', methods=['DELETE'])
@is_xhr
@is_logged
@has_permission_to_project
def delete_project(project_id):
    return execute_action(
        'app.action.admin.delete_project', None, project_id=project_id
    )


@admin_page.route('/project/sources/<project_id>/', methods=['POST'])
@is_xhr
@is_logged
@has_permission_to_project
@are_args_in_json_request(json_args=('social_network', 'restaurant_id'))
def add_data_source(project_id, json_data):
    return execute_action(
        'app.action.admin.add_data_source', None, project_id=project_id,
        json_data=json_data
    )


@admin_page.route('/project/sources/<project_id>/', methods=['PUT'])
@is_xhr
@is_logged
@has_permission_to_project
@are_args_in_json_request(json_args=('social_network', 'restaurant_id'))
def edit_data_source(project_id, json_data):
    return execute_action(
        'app.action.admin.edit_data_source', None, project_id=project_id,
        json_data=json_data
    )


@admin_page.route(
    '/project/<project_id>/review/<review_id>/sentiment/', methods=['PUT']
)
@is_xhr
@has_permission_to_project
@are_args_in_json_request(json_args=('sentiment',))
def edit_review_sentiment(project_id, review_id, json_data):
    return execute_action(
        'app.action.admin.edit_review_sentiment', None, project_id=project_id,
        review_id=review_id, json_data=json_data
    )


@admin_page.route(
    '/project/<project_id>/review/<review_id>/spam/', methods=['PUT']
)
@is_xhr
@has_permission_to_project
@are_args_in_json_request(json_args=('is_spam',))
def mark_review_as_spam(project_id, review_id, json_data):
    return execute_action(
        'app.action.admin.mark_review_as_spam', None, project_id=project_id,
        review_id=review_id, json_data=json_data
    )


@admin_page.route('/project/retrieve-data/<project_id>/', methods=['PUT'])
@is_xhr
@has_permission_to_project
def request_retrieve_data_from_social_networks(project_id):
    return execute_action(
        'app.action.request_retrieve_data_from_social_networks',
        None,
        project_id=project_id
    )


@admin_page.route('/project/analyse/<project_id>/', methods=['PUT'])
@is_xhr
@has_permission_to_project
def request_analysis(project_id):
    return execute_action(
        'app.action.request_analysis', None, project_id=project_id
    )
