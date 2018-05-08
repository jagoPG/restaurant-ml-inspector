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

from src.domain.exception import UserDoesNotExist
from src.infrastructure.query_bus import QueryHandler


class GetUserProjectsQuery(object):
    """
    Retrieves all projects from a user
    """
    def __init__(self, user_id):
        self.user_id = user_id


class GetUserProjects(QueryHandler):
    def __init__(self):
        self.project_transformer = None
        self.user_repository = None

    def invoke(self, query):
        user = self.__get_user(query.user_id)
        return self.__get_projects(user)

    def __get_user(self, user_id):
        user = self.user_repository.get_of_identifier(user_id)
        if not user:
            raise UserDoesNotExist
        return user

    def __get_projects(self, user):
        projects = user.get_projects()
        parse_projects = []
        for project in projects:
            self.project_transformer.write(project)
            parse_projects.append(
                self.project_transformer.read()
            )
        return parse_projects
