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
from uuid import uuid4

from flask import current_app
from werkzeug.exceptions import NotFound

from src.application.command.analysis.create_analysis import \
    CreateAnalysisCommand
from src.application.command.analysis.process_restaurant_overview import \
    ProcessRestaurantOverviewCommand
from src.application.command.analysis.process_restaurant_reviews import \
    ProcessRestaurantReviewsCommand
from src.application.command.analysis.remove_analysis import \
    RemoveAnalysisCommand
from src.application.query.analysis.get_analysis_of_project import \
    GetAnalysisOfProjectQuery
from src.domain.exception import ProjectDoesNotExist
from web.routing.actions.action import Action


class RequestAnalysis(Action):
    def __init__(self):
        self.command_bus = None
        self.query_bus = None

    def invoke(self, request=None, **kwargs):
        project_id = kwargs['project_id']
        try:
            self.__analyze_project(project_id)
        except ProjectDoesNotExist:
            current_app.logger.error(
                'Project {0} not found for analysis'.format(project_id)
            )
            raise NotFound
        except TimeoutError:
            current_app.logger.error(
                'Database timeout when analysing the project {0}'.format(
                    project_id
                )
            )
            return current_app.response_class(status=400, response=dumps({
                'error': 'Neo4j database timeout'
            }))
        return current_app.response_class(status=200)

    def __analyze_project(self, project_id):
        analysis = self.__check_analysis_exists(project_id)
        if analysis is not None:
            self.__remove_previous_instances(analysis['identifier'])
        analysis_id = uuid4().__str__()
        command = CreateAnalysisCommand(project_id, analysis_id)
        self.command_bus.execute(command)
        command = ProcessRestaurantOverviewCommand(project_id, analysis_id)
        self.command_bus.execute(command)
        command = ProcessRestaurantReviewsCommand(project_id)
        self.command_bus.execute(command)

    def __check_analysis_exists(self, project_id):
        query = GetAnalysisOfProjectQuery(project_id)
        return self.query_bus.execute(query)

    def __remove_previous_instances(self, analysis_id):
        command = RemoveAnalysisCommand(analysis_id)
        self.command_bus.execute(command)
