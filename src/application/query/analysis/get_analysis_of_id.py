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


class GetAnalysisOfIdQuery(object):
    """
    Gets an analysis with an identifier
    """

    def __init__(self, analysis_id):
        self.analysis_id = analysis_id


class GetAnalysisOfId(QueryHandler):
    def __init__(self):
        self.analysis_repository = None
        self.analysis_transformer = None

    def invoke(self, command):
        analysis = self.analysis_repository.get_of_id(command.analysis_id)
        if analysis is None:
            return None
        self.analysis_transformer.write(analysis)
        return self.analysis_transformer.read()

