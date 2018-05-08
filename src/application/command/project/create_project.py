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

from src.domain.model import Project
from src.infrastructure.command_bus import CommandHandler
from src.domain.exception import UserDoesNotExist
from datetime import datetime


class CreateProjectCommand(object):
    """
    Creates a new restaurant project
    """

    def __init__(self, identifier, name, description, user_identifier):
        self.identifier = identifier
        self.name = name
        self.description = description
        self.user_identifier = user_identifier


class CreateProject(CommandHandler):
    def __init__(self):
        self.project_repository = None
        self.user_repository = None

    def invoke(self, command):
        user = self.__get_user(command.user_identifier)
        project = self.__create_project(command.identifier, command.name, command.description, user)
        self.__assign_project_to_user(project, user)

    def __get_user(self, user_id):
        user = self.user_repository.get_of_identifier(user_id)
        if not user:
            raise UserDoesNotExist
        return user

    def __create_project(self, identifier, name, description, user):
        project = Project(
            identifier=identifier,
            name=name,
            description=description,
            created_on=datetime.now(),
            author=user
        )
        self.project_repository.persist(project)
        return project

    def __assign_project_to_user(self, project, user):
        user.assign_project(project)
        self.user_repository.persist(user)
