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

from src.infrastructure.command_bus import CommandHandler
from src.domain.exception import ProjectDoesNotExist, UserDoesNotExist


class DeleteProjectCommand(object):
    """
    Removes a project and all its data
    """

    def __init__(self, project_id, user_id):
        self.project_id = project_id
        self.user_id = user_id


class DeleteProject(CommandHandler):
    def __init__(self):
        self.project_repository = None
        self.user_repository = None

    def invoke(self, command):
        project = self.__retrieve_project(command.project_id)
        self.__unlink_author(project)
        self.project_repository.remove(project)

    def __get_user(self, user_id):
        user = self.user_repository.get_of_identifier(user_id)
        if not user:
            raise UserDoesNotExist
        return user

    def __unlink_author(self, project):
        if not project.author:
            raise UserDoesNotExist
        author = project.get_author()
        author.remove_project(project)
        self.user_repository.persist(author)

    def __retrieve_project(self, project_id):
        project = self.project_repository.get_of_id(project_id)
        if not project:
            raise ProjectDoesNotExist
        return project
