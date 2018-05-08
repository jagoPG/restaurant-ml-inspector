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

from src.domain.exception import ProjectDoesNotExist, AccessViolation
from src.infrastructure.query_bus import QueryHandler


class UserHasPermissionToProjectQuery(object):
    """
    Checks if an user has permission for accessing to a project
    """

    def __init__(self, project_id, user_id):
        self.project_id = project_id
        self.user_id = user_id


class UserHasPermissionToProject(QueryHandler):
    def __init__(self):
        self.project_repository = None

    def invoke(self, query):
        project = self.__retrieve_project(query.project_id)
        author = project.get_author()
        if author.identifier != query.user_id:
            raise AccessViolation

    def __retrieve_project(self, project_id):
        project = self.project_repository.get_of_id(project_id)
        if not project:
            raise ProjectDoesNotExist
        return project
