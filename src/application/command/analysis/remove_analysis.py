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

from src.domain.exception import AnalysisDoesNotExistException
from src.infrastructure.command_bus import CommandHandler


class RemoveAnalysisCommand(object):
    """
    Removes an analysis instance. This operation has to be executed before
    beginning a new analysis process.
    """
    def __init__(self, analysis_id):
        self.analysis_id = analysis_id


class RemoveAnalysis(CommandHandler):
    def __init__(self):
        self.analysis_repository = None
        self.key_point_repository = None
        self.review_repository = None
        self.restaurant_repository = None

    def invoke(self, command):
        analysis = self.retrieve_analysis(command.analysis_id)
        self.remove_key_points(analysis)
        self.remove_analysis_restaurant(analysis)
        self.remove_analysis(analysis)

    def retrieve_analysis(self, analysis_id):
        analysis = self.analysis_repository.get_of_id(analysis_id)
        if analysis is None:
            raise AnalysisDoesNotExistException()
        return analysis

    def remove_key_points(self, analysis):
        key_points = analysis.get_key_points()
        for key_point in key_points:
            self.key_point_repository.remove(key_point)

    def remove_analysis_restaurant(self, analysis):
        self.restaurant_repository.remove(analysis.restaurant.single())

    def remove_analysis(self, analysis):
        self.analysis_repository.remove(analysis)
