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
from src.domain.exception import ProjectDoesNotExist


class GetProjectOfIdQuery(object):
    """
    Gets a project with an identifier
    """
    def __init__(self, project_id):
        self.project_id = project_id


class GetProjectOfId(QueryHandler):
    def __init__(self):
        self.project_repository = None
        self.project_transformer = None

    def invoke(self, query):
        project = self.project_repository.get_of_id(query.project_id)
        if project is None:
            raise ProjectDoesNotExist
        self.project_transformer.write(project)
        return self.project_transformer.read()
