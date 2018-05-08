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


class GetProjectSourcesQuery(object):
    """
    Gets social network sources' identifiers from a project
    """
    def __init__(self, project_id):
        self.project_id = project_id


class GetProjectSources(QueryHandler):
    def __init__(self):
        self.project_repository = None

    def invoke(self, query):
        project = self.__retrieve_project(query.project_id)
        sources = self.__get_sources(project)
        return sources

    def __retrieve_project(self, project_id):
        project = self.project_repository.get_of_id(project_id)
        if project is None:
            raise ProjectDoesNotExist()
        return project

    @staticmethod
    def __get_sources(project):
        source_information = list()
        sources = project.restaurants.all()
        for source in sources:
            source = GetProjectSources.__transform_data(source)
            source_information.append(source)
        return source_information

    @staticmethod
    def __transform_data(source):
        if source.get_country():
            country_code = source.get_country().code
        else:
            country_code = None
        return {
            'restaurant_name': source.name,
            'social_network_name': source.get_source_network(),
            'restaurant_social_network_id': source.social_network_identifier,
            'country': country_code
        }

