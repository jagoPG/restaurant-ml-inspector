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

from datetime import datetime
from neomodel import cardinality
from src.domain.exception import AnalysisAlreadyCreatedException
from src.domain.model import Analysis
from src.infrastructure.command_bus import CommandHandler


class CreateAnalysisCommand(object):
    """
    Creates a new restaurant analysis for a project
    """

    def __init__(self, project_id, analysis_id=None):
        self.project_id = project_id
        self.created_on = datetime.now()
        self.analysis_id = analysis_id


class CreateAnalysis(CommandHandler):
    def __init__(self):
        self.analysis_repository = None
        self.project_repository = None

    def invoke(self, command):
        project = self.__retrieve_project(command.project_id)
        self.__check_analysis_not_created(project)
        self.__create_analysis(
            project, command.created_on, command.analysis_id
        )

    def __retrieve_project(self, project_id):
        return self.project_repository.get_of_id(project_id)

    @staticmethod
    def __check_analysis_not_created(project):
        try:
            project.analysis.single()
            raise AnalysisAlreadyCreatedException
        except cardinality.CardinalityViolation:
            pass

    def __create_analysis(self, project, created_on, analysis_id=None):
        analysis = Analysis(
            identifier=analysis_id,
            last_analysis=created_on,
            project=project
        )
        self.analysis_repository.persist(analysis)
        project.add_analysis(analysis)
        self.project_repository.persist(project)
