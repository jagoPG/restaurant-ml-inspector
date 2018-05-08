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

from flask import current_app
from werkzeug.exceptions import BadRequest

from src.application.command.data_source.edit_facebook import \
    EditFacebookSourceCommand
from src.application.command.data_source.edit_google_places import \
    EditGooglePlacesSourceCommand
from src.application.command.data_source.edit_twitter import \
    EditTwitterSourceCommand
from web.routing.actions.action import Action


class EditDataSource(Action):
    def __init__(self):
        self.command_bus = None

    def invoke(self, request=None, **kwargs):
        json_data = kwargs['json_data']
        project_id = kwargs['project_id']

        social_network = json_data['social_network']
        if social_network not in ['Google Places', 'Twitter', 'Facebook']:
            current_app.logger.warning(
                '%s social network does not exist' % social_network)
            raise BadRequest
        restaurant_id = json_data['restaurant_id']

        if social_network == 'Facebook':
            self.__check_not_null_field(json_data, 'country')
            command = EditFacebookSourceCommand(
                project_id, restaurant_id, json_data['country']
            )
        elif social_network == 'Google Places' and json_data['country'] != '':
            self.__check_not_null_field(json_data, 'country')
            command = EditGooglePlacesSourceCommand(
                project_id, restaurant_id, json_data['country']
            )
        else:
            self.__check_not_null_field(json_data, 'geo_position')
            command = EditTwitterSourceCommand(
                project_id, restaurant_id, json_data['geo_position']
            )
        if not command:
            current_app.logger.warning(
                '{0} project\'s data source edition request failed'.format(
                    project_id
                )
            )
            raise BadRequest
        self.command_bus.execute(command)
        return current_app.response_class(status=201)

    @staticmethod
    def __check_not_null_field(dictionary, field):
        if field not in dictionary or dictionary[field].strip() == '':
            raise BadRequest
