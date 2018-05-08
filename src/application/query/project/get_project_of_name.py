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

from src.infrastructure.query_bus import QueryHandler


class GetProjectOfNameQuery(object):
    """
    Retrieves all available projects
    """
    def __init__(self, name):
        self.name = name


class GetProjectOfName(QueryHandler):
    def __init__(self):
        self.project_repository = None
        self.project_transformer = None

    def invoke(self, query):
        projects = self.project_repository.get_of_name(query.name)
        parse_projects = []
        for project in projects:
            self.project_transformer.write(project)
            parse_projects.append(
                self.project_transformer.read()
            )
        return parse_projects
