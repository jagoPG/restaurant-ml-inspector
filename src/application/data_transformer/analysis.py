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


class AnalysisDataTransformer(DataTransformer):
    def read(self):
        good_key_points, improvement_key_points = self.__transform_key_points()
        restaurant = self.__transform_restaurant()
        return {
            'identifier': self.instance.identifier,
            'karma': self.instance.karma,
            'last_analysis': self.instance.last_analysis.strftime(
                '%Y-%m-%d %H:%M:%S'
            ),
            'restaurant_data': restaurant,
            'good_key_points': good_key_points,
            'improvement_key_points': improvement_key_points
        }

    def __transform_restaurant(self):
        restaurant = self.instance.restaurant.single()
        return {
            'name': restaurant.name,
            'accepts_reservation': restaurant.accepts_reservations,
            'star_rating': restaurant.star_rating,
            'opening_hours': restaurant.opening_hours,
            'address': restaurant.address,
            'telephone': restaurant.telephone,
            'description': restaurant.description
        }

    def __transform_key_points(self):
        good_key_points = []
        improvement_points = []
        for key_point in self.instance.key_points.all():
            if key_point.karma >= 0:
                good_key_points.append(
                    self.__transform_key_point(key_point)
                )
            else:
                improvement_points.append(
                    self.__transform_key_point(key_point)
                )
        return good_key_points, improvement_points

    def __transform_key_point(self, key_point):
        appearances = self.__transform_reviews(key_point)
        return {
            'identifier': key_point.identifier,
            'name': key_point.identifier,
            'karma': key_point.karma,
            'appearances': len(appearances),
            'reviews': appearances
        }

    @staticmethod
    def __transform_reviews(key_point):
        transformed_reviews = []
        for review in key_point.appearances.all():
            transformed_reviews.append({
                'reference': review.reference,
                'text': review.review_body,
                'karma': key_point.karma
            })
        return transformed_reviews
