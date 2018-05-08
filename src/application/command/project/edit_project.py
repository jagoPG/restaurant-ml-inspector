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
from src.infrastructure.command_bus import CommandHandler


class EditProjectCommand(object):
    """
    Modifies a project's data
    """

    def __init__(self, identifier, name, description):
        self.identifier = identifier
        self.name = name
        self.description = description


class EditProject(CommandHandler):
    def __init__(self):
        self.project_repository = None

    def invoke(self, command):
        project = self.__retrieve_project(command.identifier)
        self.__modify_project(command.name, command.description, project)
        self.project_repository.persist(project)

    def __retrieve_project(self, project_id):
        project = self.project_repository.get_of_id(project_id)
        if not project:
            raise ProjectDoesNotExist
        return project

    @staticmethod
    def __modify_project(name, description, project):
        project.name = name
        project.description = description
