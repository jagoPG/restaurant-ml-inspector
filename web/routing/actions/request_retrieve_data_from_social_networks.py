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

from json import dumps

from flask import current_app

from src.application.command.data_source.retrieve_facebook import \
    RetrieveFacebookDataCommand
from src.application.command.data_source.retrieve_google_places import \
    RetrieveGooglePlacesDataCommand
from src.application.command.data_source.retrieve_twitter import \
    RetrieveTwitterDataCommand
from src.application.query.project.get_project_sources import \
    GetProjectSourcesQuery
from src.social_networks.facebook import FacebookException
from web.routing.actions.action import Action


class RequestRetrieveDataFromSocialNetworks(Action):
    def __init__(self):
        self.command_bus = None
        self.query_bus = None

    def invoke(self, request=None, **kwargs):
        project_id = kwargs['project_id']

        # Retrieve set up social networks
        query = GetProjectSourcesQuery(project_id)
        sources = self.query_bus.execute(query)

        # Retrieve data from each social network
        for source in sources:
            source_name = source['social_network_name']
            network_identifier = source['restaurant_social_network_id']
            if source_name == 'Google Places':
                command = RetrieveGooglePlacesDataCommand(
                    project_id, network_identifier
                )
            elif source_name == 'Facebook':
                command = RetrieveFacebookDataCommand(
                    project_id, network_identifier
                )
            elif source_name == 'Twitter':
                command = RetrieveTwitterDataCommand(
                    network_identifier, None, project_id
                )
            else:
                continue
            try:
                self.command_bus.execute(command)
            except FacebookException as ex:
                error = 'Facebook error: {0}'.format(ex)
                current_app.logger.error(error)
                return current_app.response_class(status=400, response=dumps({
                    'error': error
                }))
        return current_app.response_class(status=200)
