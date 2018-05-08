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


class RestaurantAnalysisDataTransformer(DataTransformer):
    """
    Transforms project data a dict with plain data
    """

    def read(self):
        return {
            'identifier': self.instance.identifier,
            'name': self.instance.name,
            'accepts_reservations': self.instance.accepts_reservations,
            'star_rating': self.instance.star_rating,
            'opening_hours': self.instance.opening_hours,
            'address': self.instance.address,
            'telephone': self.instance.telephone,
            'description': self.instance.description
        }
