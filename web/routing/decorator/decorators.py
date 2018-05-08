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

import json
from functools import wraps
from flask import request, session, current_app
from src.application.query.user.check_api_key import CheckApiKeyQuery
from src.application.query.user.get_user import GetUserQuery
from src.application.query.user.get_user_role import GetUserRoleQuery
from src.application.query.user.has_permission_to_project import \
    UserHasPermissionToProjectQuery
from src.domain.exception import AccessViolation, ApiKeyDoesNotExist, \
    UserDoesNotExist, ProjectDoesNotExist
from werkzeug.exceptions import BadRequest, Forbidden, NotFound


def is_xhr(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        is_xhr_request = 'X-Requested-With' in request.headers and \
           request.headers['X-Requested-With'] == 'XMLHttpRequest'
        if not is_xhr_request:
            current_app.logger.warning(
                'Non ajax request was received: {0}'.format(request.path)
            )
            raise BadRequest
        return f(*args, **kwargs)
    return wrapper


def is_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_identifier' not in session:
            current_app.logger.warning(
                'Access violation to: {0}'.format(request.path)
            )
            raise Forbidden
        identifier = session['user_identifier']
        query_bus = __get_query_bus()
        query = GetUserRoleQuery(identifier)
        roles = query_bus.execute(query)
        if 'ADMIN' not in roles:
            current_app.logger.warning(
                'Access violation to: {0}'.format(request.path)
            )
            raise Forbidden
        return f(*args, **kwargs)
    return wrapper


def has_valid_api_key(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not request.args or 'api_key' not in request.args:
            current_app.logger.warning(
                'Request has no attached API key: {0}'.format(request.path)
            )
            raise BadRequest
        query_bus = __get_query_bus()
        api_key = request.args['api_key']
        try:
            query_bus.execute(
                CheckApiKeyQuery(api_key)
            )
        except ApiKeyDoesNotExist:
            current_app.logger.warning('API key not valid: {0}'.format(api_key))
            raise BadRequest
        return fn(*args, **kwargs)
    return wrapper


def has_permission_to_project(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        project_id = kwargs['project_id']
        user_id = session['user_identifier']
        query_bus = __get_query_bus()
        try:
            query_bus.execute(
                UserHasPermissionToProjectQuery(project_id, user_id)
            )
        except AccessViolation:
            current_app.logger.warning(
                'Access violation to: {0}'.format(request.path)
            )
            raise Forbidden
        except ProjectDoesNotExist:
            current_app.logger.warning(
                'Project does not exist: {0}'.format(request.path)
            )
            raise NotFound
        return fn(*args, **kwargs)
    return wrapper


def is_logged(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_identifier' not in session:
            raise Forbidden
        query_bus = __get_query_bus()
        query = GetUserQuery(session['user_identifier'])
        try:
            user = query_bus.execute(query)
        except UserDoesNotExist:
            raise Forbidden
        if 'BUSINESSMAN' not in user['roles'] and 'ADMIN' not in user['roles']:
            raise Forbidden
        return fn(*args, **kwargs)
    return wrapper


def are_args_in_json_request(json_args=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.data is None:
                current_app.logger.warning(
                    'No data attached: {0}'.format(request.path)
                )
                raise BadRequest
            json_data = json.loads(request.data)
            for arg in json_args:
                if arg not in json_data:
                    current_app.logger.warning(
                        'Malformed request: {0}'.format(request.path)
                    )
                    raise BadRequest
            kwargs['json_data'] = json_data
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def are_args_in_query(query_args=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not query_args:
                current_app.logger.warning(
                    'Malformed request: {0}'.format(request.path)
                )
                raise BadRequest
            for arg in query_args:
                if arg not in request.args:
                    current_app.logger.warning(
                        'Malformed request: {0}'.format(request.path)
                    )
                    raise BadRequest
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def __get_query_bus():
    dependency_injector = current_app.config['dependency_injector']
    return dependency_injector.get('app.query_bus')
