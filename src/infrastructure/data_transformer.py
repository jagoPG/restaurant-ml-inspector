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

from src.infrastructure.dependency_injector import Dependency


class DataTransformer(Dependency):
    """
    This class transforms a domain object to a plain data object to retrieve
    data to the user
    """
    instance = None

    def write(self, instance):
        self.instance = instance

    def read(self):
        """
        :return: return a dict with the information of the class in a plain
        format
        """
        raise NotImplementedError
