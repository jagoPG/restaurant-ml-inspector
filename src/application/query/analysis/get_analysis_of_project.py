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

from src.domain.exception import ProjectDoesNotExist
from src.infrastructure.query_bus import QueryHandler


class GetAnalysisOfProjectQuery(object):
    """
    Gets an analysis from a project
    """

    def __init__(self, project_id):
        self.project_id = project_id


class GetAnalysisOfProject(QueryHandler):
    def __init__(self):
        self.project_repository = None
        self.analysis_transformer = None

    def invoke(self, command):
        project = self.project_repository.get_of_id(command.project_id)
        if project is None:
            raise ProjectDoesNotExist()
        if not len(project.analysis):
            return None
        analysis = project.analysis.single()
        self.analysis_transformer.write(analysis)
        return self.analysis_transformer.read()

