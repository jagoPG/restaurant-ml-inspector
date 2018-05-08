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

from src.domain.model import SocialNetwork, Review, Project, Analysis,\
    SocialNetworkRestaurant, Country, AnalysisRestaurant, Keyword, User
from src.domain.repository import SocialNetworkRepository,\
    RestaurantRepository, ProjectRepository, ReviewRepository,\
    AnalysisRepository, KeyPointRepository, CountryRepository,\
    KeywordRepository, UserRepository
from src.infrastructure.dependency_injector import Dependency


class Neo4jSocialNetworkRepository(SocialNetworkRepository, Dependency):
    def persist(self, instance):
        instance.save()

    def remove(self, instance):
        instance.delete()

    def get_of_name(self, name):
        return SocialNetwork.nodes.get(name=name)


class Neo4jSocialNetworkRestaurantRepository(RestaurantRepository, Dependency):
    def persist(self, instance):
        instance.save()

    def remove(self, restaurant):
        if len(restaurant.review):
            for review in restaurant.review.all():
                review.delete()
        restaurant.delete()

    @staticmethod
    def remove_reviews(restaurant):
        if len(restaurant.review):
            for review in restaurant.review.all():
                review.delete()

    @staticmethod
    def get_of_id(identifier):
        return SocialNetworkRestaurant.nodes.get_or_none(identifier=identifier)

    def get_of_name(self, social_network, name):
        return social_network.restaurants.get(name=name)


class Neo4jAnalysisRestaurantRepository(RestaurantRepository, Dependency):
    def persist(self, instance):
        instance.save()

    def remove(self, restaurant):
        restaurant.delete()

    def get_of_name(self, analysis, name):
        return analysis.restaurant.get(name=name)

    def all(self):
        return AnalysisRestaurant.nodes.all()


class Neo4jReviewRepository(ReviewRepository, Dependency):
    def persist(self, instance):
        instance.save()

    def remove(self, review):
        review.delete()

    def get_of_id(self, reference):
        return Review.nodes.get_or_none(reference=reference)

    def get_scored_reviews(self):
        return Review.nodes.filter(
            is_spam__ne=True, is_spam__isnull=True, sentiment__isnull=False
        )


class Neo4jProjectRepository(ProjectRepository, Dependency):
    def persist(self, instance):
        instance.save()

    def remove(self, instance):
        self.__delete_project_node(instance)

    def get_of_name(self, name):
        return Project.nodes.get_or_none(name=name)

    def get_of_id(self, identifier):
        return Project.nodes.get_or_none(identifier=identifier)

    def all(self):
        return Project.nodes.all()

    # Delete nodes functions
    @staticmethod
    def __delete_project_node(project):
        if len(project.restaurants):
            for restaurant in project.restaurants.all():
                Neo4jProjectRepository.__delete_restaurant_node(restaurant)
            if len(project.analysis):
                Neo4jProjectRepository.__delete_analysis_node(
                    project.analysis.single()
                )
        project.delete()

    @staticmethod
    def __delete_restaurant_node(restaurant):
        if len(restaurant.review):
            for review in restaurant.review.all():
                review.delete()
        restaurant.delete()

    @staticmethod
    def __delete_analysis_node(analysis):
        if len(analysis.key_points):
            for key_point in analysis.key_points.all():
                key_point.delete()
        if len(analysis.restaurant):
            analysis.restaurant.single().delete()
        analysis.delete()


class Neo4jAnalysisRepository(AnalysisRepository, Dependency):
    def persist(self, instance):
        instance.save()

    def remove(self, instance):
        instance.delete()

    def get_of_id(self, identifier):
        return Analysis.nodes.get_or_none(identifier=identifier)


class Neo4jKeyPointRepository(KeyPointRepository, Dependency):
    def persist(self, instance):
        instance.save()

    def remove(self, instance):
        instance.delete()


class Neo4jCountryRepository(CountryRepository):
    def all(self):
        return Country.nodes.all()

    def persist(self, country):
        country.save()

    def get_of_code(self, code):
        return Country.nodes.get_or_none(code=code)


class Neo4jKeywordRepository(KeywordRepository):
    def persist(self, keyword):
        keyword.save()

    def remove(self, keyword):
        keyword.delete()

    def get_of_name(self, name, language):
        return Keyword.nodes.get_or_none(word=name, language=language)

    def get_word_like(self, name, language):
        return Keyword.nodes.filter(
            word__iexact=name,
            language=language
        )

    def get_of_file_reference(self, file_reference, language):
        keyword = Keyword.nodes.filter(
            file_reference=file_reference,
            language=language
        ).all()
        if len(keyword):
            return keyword[0]
        else:
            return None

    def get_all(self):
        return Keyword.nodes.all()


class Neo4jUserRepository(UserRepository):
    def persist(self, user):
        user.save()

    def remove(self, user):
        user.delete()

    def all(self):
        return User.nodes.all()

    def activate_user(self, user):
        user.is_verified = True
        self.persist(user)

    def deactivate_user(self, user):
        user.is_verified = False
        self.persist(user)

    def get_of_identifier(self, identifier):
        return User.nodes.get_or_none(identifier=identifier)

    def get_of_api_key(self, api_key):
        return User.nodes.get_or_none(api_key=api_key)
