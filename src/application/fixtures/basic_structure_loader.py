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

import json
import logging

from src.application.command.country.create_country import CreateCountryCommand
from src.application.command.social_network.create_social_network import \
    CreateSocialNetworkCommand
from src.application.query.country.get_countries import GetCountriesQuery
from src.domain.model import SocialNetwork
from src.infrastructure.dependency_injector import Dependency


class BasicStructureLoader(Dependency):
    def __init__(self):
        self.command_bus = None
        self.query_bus = None
        self.keyword_loader = None
        self.country_repository = None
        self.keyword_repository = None
        self.social_network_repository = None

    def execute(self):
        if not self.__are_social_networks_created():
            self.__create_social_networks()
        if not self.__are_countries_created():
            self.__create_countries()
        if not self.__are_keywords_created():
            self.__create_keywords()

    def __are_countries_created(self):
        countries = self.query_bus.execute(GetCountriesQuery())
        return len(countries) > 0

    def __are_social_networks_created(self):
        try:
            google = self.social_network_repository.get_of_name('Google Places')
            facebook = self.social_network_repository.get_of_name('Facebook')
            twitter = self.social_network_repository.get_of_name('Twitter')
        except SocialNetwork.DoesNotExist:
            return False
        return google and facebook and twitter

    def __are_keywords_created(self):
        keywords = self.keyword_repository.get_all()
        return len(keywords) > 0

    def __create_social_networks(self):
        logging.debug('Create social networks')
        command = CreateSocialNetworkCommand(
            'Facebook', 'https://www.facebook.com'
        )
        self.command_bus.execute(command)
        command = CreateSocialNetworkCommand(
            'Twitter', 'https://www.twitter.com'
        )
        self.command_bus.execute(command)
        command = CreateSocialNetworkCommand(
            'Google Places', 'https://www.google.com/maps'
        )
        self.command_bus.execute(command)

    def __create_keywords(self):
        logging.debug('Load stored domain keywords')
        self.keyword_loader.execute()

    def __create_countries(self):
        logging.debug('Load file stored countries')
        with open('./src/application/data/country.json', 'r') as file:
            read_data = file.read()
        countries = json.loads(read_data)
        for key, country in countries.items():
            command = CreateCountryCommand(key, country)
            self.command_bus.execute(command)