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
from scipy.spatial import distance


class GetNearbyRestaurantsQuery(object):
    """
    Gets restaurants that are in a distance range from the latitude and
    longitude provided
    """

    def __init__(self, latitude, longitude, limit_distance):
        self.latitude = latitude
        self.longitude = longitude
        self.limit_distance = limit_distance


class GetNearbyRestaurants(QueryHandler):
    KILOMETERS = 6371

    def __init__(self):
        self.project_repository = None

    def invoke(self, query):
        restaurants = self.__retrieve_restaurants()
        return self.__retrieve_near_restaurants(
            restaurants, query.latitude, query.longitude, query.limit_distance
        )

    def __retrieve_restaurants(self):
        return self.project_repository.all()

    @staticmethod
    def __retrieve_near_restaurants(
            projects, user_latitude, user_longitude, max_distance
    ):
        results = list()
        for project in projects:
            restaurant = GetNearbyRestaurants.__retrieve_restaurant(project)
            if not restaurant:
                continue
            is_near = GetNearbyRestaurants.__is_restaurant_near(
                restaurant, user_latitude, user_longitude, max_distance
            )
            if is_near:
                coordinates = restaurant.geo.split(',')
                results.append({
                    'identifier': project.identifier,
                    'latitude': float(coordinates[0]),
                    'longitude': float(coordinates[1])
                })
        return results

    @staticmethod
    def __retrieve_restaurant(project):
        analysis = project.get_analysis()
        if not analysis:
            return None
        return analysis.get_restaurant()

    @staticmethod
    def __is_restaurant_near(
            restaurant, user_latitude, user_longitude, limit_distance
    ):
        if restaurant.geo is None:
            return False
        coordinates = restaurant.geo.split(',')
        two_point_distance = distance.euclidean(
            (float(user_latitude), float(user_longitude)),
            (float(coordinates[0]), float(coordinates[1]))
        ) * 100
        return limit_distance > two_point_distance
