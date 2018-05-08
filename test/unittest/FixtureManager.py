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

from src.application.command.analysis.create_analysis import \
    CreateAnalysisCommand
from src.application.command.analysis.process_restaurant_overview import \
    ProcessRestaurantOverviewCommand
from src.application.command.analysis.process_restaurant_reviews import \
    ProcessRestaurantReviewsCommand
from src.application.command.data_source.add_facebook import \
    AddFacebookSourceCommand
from src.application.command.data_source.add_google_places import \
    AddGooglePlacesSourceCommand
from src.application.command.data_source.add_twitter import \
    AddTwitterSourceCommand
from src.application.command.data_source.retrieve_facebook import \
    RetrieveFacebookDataCommand
from src.application.command.data_source.retrieve_google_places import \
    RetrieveGooglePlacesDataCommand
from src.application.command.data_source.retrieve_twitter import \
    RetrieveTwitterDataCommand
from src.application.command.project.create_project import CreateProjectCommand
from src.application.command.project.delete_project import DeleteProjectCommand
from src.application.command.user.activate_user import ActivateUserCommand
from src.application.command.user.create_user import CreateUserCommand
from src.application.command.user.remove_user import RemoveUserCommand
from src.application.command.user.update_role import UpdateUserRoleCommand
from uuid import uuid4

from src.application.query.project.get_project_sources import \
    GetProjectSourcesQuery
from src.social_networks.facebook import FacebookException


class FixtureManager(object):
    def __init__(self, dependency_injector):
        self.command_bus = dependency_injector.get('app.command_bus')
        self.query_bus = dependency_injector.get('app.query_bus')
        self.project_repository = dependency_injector.get(
            'app.repository.project'
        )

    def set_up(self):
        self.__create_users()
        self.__create_fixture_project()
        self.__set_up_project_sources()
        self.__retrieve_data('f886388e-8f38-4463-8e72-f725c3218379')
        self.__retrieve_data('f1d6328e-8f98-2163-8e12-f7a523218379')
        self.__do_analysis('f886388e-8f38-4463-8e72-f725c3218379')
        self.__do_analysis('f1d6328e-8f98-2163-8e12-f7a523218379')

    def tear_down(self):
        self.__remove_projects()
        self.__remove_users()

    def __create_users(self):
        command = CreateUserCommand(
            'admin', 'admin@example.com', 'Admin', 'Test'
        )
        self.command_bus.execute(command)
        command = UpdateUserRoleCommand(
            'admin', ['ADMIN']
        )
        self.command_bus.execute(command)
        command = CreateUserCommand(
            'client', 'client@example.com', 'Client', 'Test'
        )
        self.command_bus.execute(command)
        command = ActivateUserCommand('admin')
        self.command_bus.execute(command)
        command = ActivateUserCommand('client')
        self.command_bus.execute(command)
        command = UpdateUserRoleCommand(
            'client', ['BUSINESSMAN']
        )
        self.command_bus.execute(command)

    def __create_fixture_project(self):
        command = CreateProjectCommand(
            'f886388e-8f38-4463-8e72-f725c3218379', 'El Ampli', '', 'admin'
        )
        self.command_bus.execute(command)
        command = CreateProjectCommand(
            'f1d6328e-8f98-2163-8e12-f7a523218379',
            'Restaurante Sakura',
            '',
            'client'
        )
        self.command_bus.execute(command)

    def __set_up_project_sources(self):
        self.__launch_project_sources_command(
            'Facebook',
            'f886388e-8f38-4463-8e72-f725c3218379',
            '230390187297922'
        )
        self.__launch_project_sources_command(
            'Google Places',
            'f886388e-8f38-4463-8e72-f725c3218379',
            'ChIJayu_kXBaTg0R6sIoWp7K5cY'
        )
        self.__launch_project_sources_command(
            'Twitter',
            'f886388e-8f38-4463-8e72-f725c3218379',
            'El Ampli Barakaldo'
        )
        self.__launch_project_sources_command(
            'Facebook',
            'f1d6328e-8f98-2163-8e12-f7a523218379',
            '143720722690776'
        )
        self.__launch_project_sources_command(
            'Google Places',
            'f1d6328e-8f98-2163-8e12-f7a523218379',
            'ChIJZz5MGXRaTg0RqkxfpYV6rdA'
        )
        self.__launch_project_sources_command(
            'Twitter',
            'f1d6328e-8f98-2163-8e12-f7a523218379',
            '@rest_japones'
        )

    def __launch_project_sources_command(
            self, social_network, project_id, place_identifier
    ):
        if social_network == 'Facebook':
            command = AddFacebookSourceCommand(
                project_id, place_identifier, 'ES'
            )
        elif social_network == 'Google Places':
            command = AddGooglePlacesSourceCommand(
                project_id, place_identifier, 'ES'
            )
        else:
            command = AddTwitterSourceCommand(
                project_id, place_identifier, 'ES'
            )
        self.command_bus.execute(command)

    def __retrieve_data(self, project_id):
        query = GetProjectSourcesQuery(project_id)
        sources = self.query_bus.execute(query)
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
                logging.critical('Facebook error: %s' % ex.args)

    def __do_analysis(self, project_id):
        analysis_id = uuid4().__str__()
        command = CreateAnalysisCommand(project_id)
        self.command_bus.execute(command)
        command = ProcessRestaurantOverviewCommand(project_id, analysis_id)
        self.command_bus.execute(command)
        command = ProcessRestaurantReviewsCommand(project_id)
        self.command_bus.execute(command)

    def __remove_users(self):
        command = RemoveUserCommand('admin')
        self.command_bus.execute(command)
        command = RemoveUserCommand('client')
        self.command_bus.execute(command)

    def __remove_projects(self):
        command = DeleteProjectCommand(
            'f886388e-8f38-4463-8e72-f725c3218379', 'admin'
        )
        self.command_bus.execute(command)
        command = DeleteProjectCommand(
            'f1d6328e-8f98-2163-8e12-f7a523218379', 'client'
        )
        self.command_bus.execute(command)

