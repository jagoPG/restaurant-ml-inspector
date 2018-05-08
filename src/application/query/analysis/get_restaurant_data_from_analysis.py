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
from src.domain.exception import ProjectDoesNotExist, \
    AnalysisDoesNotExistException


class GetRestaurantDataFromAnalysisQuery(object):
    """
    Gets analysed data from restaurant analysis
    """
    def __init__(self, project_id):
        self.project_id = project_id


class GetRestaurantDataFromAnalysis(QueryHandler):
    def __init__(self):
        self.project_repository = None
        self.restaurant_analysis_transformer = None

    def invoke(self, query):
        project = self.__retrieve_project(query.project_id)
        analysis = self.__retrieve_analysis(project)
        return self.__retrieve_restaurant(analysis)

    def __retrieve_project(self, project_id):
        project = self.project_repository.get_of_id(project_id)
        if project is None:
            raise ProjectDoesNotExist()
        return project

    @staticmethod
    def __retrieve_analysis(project):
        analysis = project.analysis
        if not len(analysis):
            raise AnalysisDoesNotExistException()
        return analysis.single()

    def __retrieve_restaurant(self, analysis):
        restaurant = analysis.restaurant
        if not len(restaurant):
            return {}
        self.restaurant_analysis_transformer.write(restaurant.single())
        return self.restaurant_analysis_transformer.read()
