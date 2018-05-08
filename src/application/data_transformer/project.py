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

from src.infrastructure.data_transformer import DataTransformer


class ProjectDataTransformer(DataTransformer):
    """
    Transforms project data a dict with plain data
    """

    def read(self):
        created_on = self.instance.created_on
        if created_on:
            created_on = created_on.strftime('%Y-%m-%d %H:%M:%S')

        analysis_identifier = self.__transform_analysis_id()
        return {
            'identifier': self.instance.identifier,
            'name': self.instance.name,
            'description': self.instance.description,
            'created_on': created_on,
            'analysis_id': analysis_identifier
        }

    def __transform_analysis_id(self):
        if len(self.instance.analysis):
            return self.instance.analysis.single().identifier
        else:
            return None
