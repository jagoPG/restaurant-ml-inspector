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

from uuid import uuid4
from neomodel import StructuredNode, StringProperty, BooleanProperty,\
    FloatProperty, RelationshipTo, RelationshipFrom, One, ZeroOrMore,\
    DateTimeProperty, ArrayProperty
from src.domain.exception import RoleDoesNotExist


class Review(StructuredNode):
    """
    Represents a user opinion downloaded from a social network about a
    restaurant

    Source: http://schema.org/Review
    """
    reference = StringProperty(unique_index=True, default=uuid4)
    identifier = StringProperty(unique_index=True, default=uuid4)
    item_reviewed = RelationshipFrom(
        'SocialNetworkRestaurant', 'REVIEW', cardinality=One
    )
    review_body = StringProperty()
    appearances = RelationshipFrom(
        'KeyPoint', 'REVIEW_POINT', cardinality=ZeroOrMore
    )
    is_spam = BooleanProperty()
    sentiment = FloatProperty()

    def add_key_point(self, key_point):
        self.appearances.connect(key_point)

    def is_from_project(self, project_id):
        return self.item_reviewed.single().\
                   from_project.single().\
                   identifier == project_id


class Restaurant(StructuredNode):
    """
    Represents general information about a restaurant

    Source: http://schema.org/Restaurant
    """
    __abstract_node__ = True
    identifier = StringProperty(unique_index=True, default=uuid4)
    name = StringProperty()
    accepts_reservations = BooleanProperty()
    star_rating = FloatProperty()
    opening_hours = StringProperty()
    address = StringProperty()
    telephone = StringProperty()
    description = StringProperty()
    from_project = RelationshipFrom(
        'Project', 'RESTAURANT_PROJECT', cardinality=ZeroOrMore
    )
    geo = StringProperty()


class SocialNetworkRestaurant(Restaurant):
    """
    This Restaurant instance stores data from the Social Networks
    """
    review = RelationshipTo('Review', 'REVIEW', cardinality=ZeroOrMore)
    source_network = RelationshipFrom(
        'SocialNetwork', 'RESTAURANT', cardinality=One
    )
    social_network_identifier = StringProperty()
    country = RelationshipTo('Country', 'COUNTRY_RESTAURANT', cardinality=One)

    def get_country(self):
        if len(self.country) == 1:
            return self.country.single()
        return None

    def get_source_network(self):
        return self.source_network.single().name

    def add_review(self, review):
        self.review.connect(review)

    def get_reviews(self):
        return self.review.all()

    def get_review_of_id(self, review_id):
        return self.review.get_or_none(identifier=review_id)


class AnalysisRestaurant(Restaurant):
    """
    This Restaurant instance stores data from the analysed restaurants
    """
    source_project = RelationshipFrom(
        'Project', 'RESTAURANT_ANALYSIS', cardinality=One
    )
    analysis = RelationshipFrom(
        'Analysis', 'RESTAURANT_ANALYSIS', cardinality=One
    )

    def get_project_id(self):
        return self.analysis.single().get_project_id()


class SocialNetwork(StructuredNode):
    """
    Social Network model. This contains restaurant data extracted from the
    social network instance
    """
    identifier = StringProperty(unique_index=True)
    name = StringProperty()
    restaurants = RelationshipTo(
        'SocialNetworkRestaurant', 'RESTAURANT', cardinality=ZeroOrMore
    )

    def has_restaurant(self, restaurant):
        return self.restaurants.is_connected(restaurant)

    def add_restaurant(self, restaurant):
        return self.restaurants.connect(restaurant)

    def get_restaurant_of_id(self, social_network_id):
        return self.restaurants.get_or_none(
            social_network_identifier=social_network_id
        )

    def remove_restaurant(self, restaurant):
        self.restaurants.disconnect(restaurant)


class Project(StructuredNode):
    """
    A project contains the restaurants that have been generated from a query.
    """
    identifier = StringProperty(unique_index=True)
    name = StringProperty(unique_index=True)
    description = StringProperty()
    restaurants = RelationshipTo(
        'SocialNetworkRestaurant', 'RESTAURANT_PROJECT', cardinality=ZeroOrMore
    )
    social_networks = RelationshipTo(
        'SocialNetwork', 'SOCIAL_NETWORK', cardinality=ZeroOrMore
    )
    created_on = DateTimeProperty()
    analysis = RelationshipTo('Analysis', 'PROJECT', cardinality=One)
    author = RelationshipFrom('User', 'USER_PROJECT', cardinality=One)

    def get_analysis(self):
        if len(self.analysis):
            return self.analysis.single()
        return None

    def get_restaurants(self):
        return self.restaurants.all()

    def add_social_network(self, social_network):
        self.social_networks.connect(social_network)

    def add_restaurant(self, restaurant):
        self.restaurants.connect(restaurant)
        restaurant.from_project.connect(self)

    def add_analysis(self, analysis):
        self.analysis.connect(analysis)

    def get_author(self):
        return self.author.single()


class KeyPoint(StructuredNode):
    """
    Scored keywords that have been found during a restaurant analysis. The
    review where the keyword was found is linked to the instance
    """
    identifier = StringProperty(unique_index=True, default=uuid4)
    word = StringProperty()
    karma = FloatProperty()
    appearances = RelationshipTo(
        'Review', 'REVIEW_POINT', cardinality=ZeroOrMore
    )
    analysis = RelationshipTo('Analysis', 'KEY_POINTS', cardinality=One)

    def add_review(self, review):
        self.appearances.connect(review)


class Analysis(StructuredNode):
    """
    Stores general analysis information of a restaurant
    """
    identifier = StringProperty(unique_index=True, default=uuid4)
    karma = FloatProperty()
    last_analysis = DateTimeProperty()
    project_rel = RelationshipFrom('Project', 'ANALYSIS', cardinality=One)
    key_points = RelationshipFrom(
        'KeyPoint', 'KEY_POINTS', cardinality=ZeroOrMore
    )
    restaurant = RelationshipTo(
        'AnalysisRestaurant', 'RESTAURANT_ANALYSIS', cardinality=One
    )

    def add_key_point(self, key_point):
        self.key_points.connect(key_point)

    def add_restaurant(self, restaurant):
        self.restaurant.connect(restaurant)

    def get_restaurant(self):
        return self.restaurant.single()

    def get_key_points(self):
        return self.key_points.all()


class Country(StructuredNode):
    """
    Represents a Country
    """
    code = StringProperty(unique_index=True)
    name = StringProperty()
    restaurants = RelationshipFrom(
        'SocialNetworkRestaurant', 'COUNTRY_RESTAURANT', cardinality=ZeroOrMore
    )

    def add_restaurant(self, restaurant):
        self.restaurants.connect(restaurant)

    def remove_restaurant(self, restaurant):
        self.restaurants.disconnect(restaurant)


class Keyword(StructuredNode):
    """
    Represents a domain keyword that is wanted to be detected during the
    analysis process
    """
    word = StringProperty(unique_index=True)
    language = StringProperty()
    synonym = RelationshipTo('Keyword', 'SYNONYM', cardinality=ZeroOrMore)
    translation = RelationshipTo(
        'Keyword', 'TRANSLATION', cardinality=ZeroOrMore
    )
    file_reference = StringProperty()

    def add_synonym(self, synonym):
        self.synonym.connect(synonym)

    def add_translation(self, word):
        if word.language == self.language:
            raise SyntaxError()
        self.translation.connect(word)

    def are_synonyms(self, word):
        return self.synonym.is_connected(word)

    def are_translations(self, word):
        return self.translation.is_connected(word)


class User(StructuredNode):
    """
    Represents an user that can access to the platform
    """
    email = StringProperty(unique_index=True)
    identifier = StringProperty(unique_index=True)
    name = StringProperty()
    surnames = StringProperty()
    last_login = DateTimeProperty()
    projects = RelationshipTo('Project', 'USER_PROJECT', cardinality=ZeroOrMore)
    is_verified = BooleanProperty()
    roles = ArrayProperty()
    api_key = StringProperty()

    def get_projects(self):
        if len(self.projects) == 0:
            return []
        else:
            return self.projects.all()

    def grant_role(self, role):
        if role not in User.get_roles():
            raise RoleDoesNotExist()
        if self.roles:
            if role not in self.roles:
                self.roles.append(role)
        else:
            self.roles = [role]

    def revoke_role(self, role):
        if role not in User.get_roles():
            raise RoleDoesNotExist()
        if self.roles:
            if role in self.roles:
                self.roles.remove(role)

    def assign_project(self, project):
        self.projects.connect(project)

    def remove_project(self, project):
        self.projects.disconnect(project)

    @staticmethod
    def get_roles():
        return [
            'ADMIN', 'BUSINESSMAN', 'DEVELOPER'
        ]
