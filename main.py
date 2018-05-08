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
import sys
from uuid import uuid4

from neo4j.exceptions import ServiceUnavailable
from neomodel import config
from tabulate import tabulate

from src.application.command.analysis.create_analysis import \
    CreateAnalysisCommand
from src.application.command.analysis.process_restaurant_overview import \
    ProcessRestaurantOverviewCommand
from src.application.command.analysis.process_restaurant_reviews import \
    ProcessRestaurantReviewsCommand
from src.application.command.analysis.remove_analysis import \
    RemoveAnalysisCommand
from src.application.command.country.create_country import CreateCountryCommand
from src.application.command.data_source.retrieve_facebook import \
    RetrieveFacebookDataCommand
from src.application.command.data_source.retrieve_google_places import \
    RetrieveGooglePlacesDataCommand
from src.application.command.data_source.retrieve_twitter import \
    RetrieveTwitterDataCommand
from src.application.command.keyword.create_keyword import \
    CreateKeywordCommand, KeywordAlreadyCreatedException
from src.application.command.project.create_project import CreateProjectCommand
from src.application.command.social_network.create_social_network import \
    CreateSocialNetworkCommand
from src.application.config import NEO4J_CONFIG
from src.application.query.analysis.get_analysis_of_id import \
    GetAnalysisOfIdQuery
from src.application.query.analysis.get_analysis_of_project import \
    GetAnalysisOfProjectQuery
from src.application.query.data_sources.retrieve_facebook_id import \
    RetrieveFacebookIdQuery
from src.application.query.data_sources.retrieve_google_places_id import \
    RetrieveGooglePlacesIdQuery
from src.application.query.project.get_project_of_id import GetProjectOfIdQuery
from src.application.query.project.get_projects import GetProjectsQuery
from src.domain.exception import RestaurantNotFoundInFacebook, \
    RestaurantNotFoundInGooglePlaces
from src.infrastructure.dependency_injector import DependencyInjector


# Set up database connection
config.DATABASE_URL = 'bolt://%s:%s@localhost:7687' % (
    NEO4J_CONFIG['user'], NEO4J_CONFIG['passwd']
)

# The identifier of an stored user in the current application
APP_USER_IDENTIFIER = ''


class Main(object):
    """
    This class allows to test the basic operations of the platform. Before
    any action is performed, countries and keywords should have been launched.
    """
    projects = {}

    def __init__(self):
        self.dependency_injector = DependencyInjector()
        self.command_bus = self.dependency_injector.get('app.command_bus')
        self.query_bus = self.dependency_injector.get('app.query_bus')
        self.google_client = self.dependency_injector.get(
            'app.social_networks.google_places'
        )
        self.facebook_client = self.dependency_injector.get(
            'app.social_networks.facebook'
        )
        self.twitter_client = self.dependency_injector.get(
            'app.social_networks.twitter'
        )
        try:
            self.social_network_repository = self.dependency_injector.get(
                'app.repository.social_network'
            )
            self.restaurant_repository = self.dependency_injector.get(
                'app.repository.social_network_restaurant'
            )
            self.review_repository = self.dependency_injector.get(
                'app.repository.review'
            )
            self.project_repository = self.dependency_injector.get(
                'app.repository.project'
            )
            self.analysis_repository = self.dependency_injector.get(
                'app.repository.analysis'
            )
        except ServiceUnavailable:
            print('[Error] Neo4j database is not running')
            sys.exit(0)
        self.__create_social_network_nodes()

    def __create_social_network_nodes(self):
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

    def create_project(self, identifier, project_name):
        command = CreateProjectCommand(
            identifier, project_name, '', APP_USER_IDENTIFIER
        )
        self.command_bus.execute(command)

    @staticmethod
    def request_operation():
        print('1. Create new project')
        print('2. Download analysis data')
        print('3. Analyze project')
        print('4. Add keywords')
        print('5. Synonyms')
        print('6. Show analysis results')
        print('7. Load countries')
        print('8. Load keywords')
        print('9. Exit')

        return input('Operation [1-9]: ')

    @staticmethod
    def request_project_name():
        return input('Input project name: ')

    @staticmethod
    def request_facebook_information():
        print('Input facebook information')
        restaurant_name = input('Type the restaurant name: ')
        country = input('Type the country: ')
        return restaurant_name, country

    @staticmethod
    def request_google_information():
        print('Input Google Places information')
        restaurant_name = input('Type the restaurant name: ')
        country = input('Type the country: ')
        return restaurant_name, country

    @staticmethod
    def request_twitter_information():
        print('Input Twitter information')
        restaurant_name = input('Twitter username: ')
        location = input('Coordinates: ')

        return restaurant_name, location

    def download_social_data(self, project_id):
        operation = None

        while operation != 4:
            print('1. Google Places')
            print('2. Facebook')
            print('3. Twitter')
            print('4. Back')
            operation = int(input('Social Network: '))

            if operation == 1:
                place_name, country = self.request_google_information()
                try:
                    query = RetrieveGooglePlacesIdQuery(place_name, country)
                    identifiers = self.query_bus.execute(query)
                except RestaurantNotFoundInGooglePlaces:
                    print('[INFO] Restaurant not found in Google')
                    continue
                command = RetrieveGooglePlacesDataCommand(
                    project_id, identifiers[0]
                )
            elif operation == 2:
                place_name, country = self.request_facebook_information()
                try:
                    query = RetrieveFacebookIdQuery(place_name, country)
                    facebook_id = self.query_bus.execute(query)
                    command = RetrieveFacebookDataCommand(
                        project_id, facebook_id
                    )
                except RestaurantNotFoundInFacebook:
                    print('[INFO] Restaurant not found in Facebook')
                    continue
            elif operation == 3:
                place_name, location = self.request_twitter_information()
                command = RetrieveTwitterDataCommand(
                    place_name, location, project_id
                )
            else:
                break
            try:
                self.command_bus.execute(command)
            except TimeoutError:
                print('Cannot connect to the social network')

    def analyze_project(self, project_id):
        analysis = self.check_analysis_exists(project_id)
        if analysis is not None:
            self.remove_previous_instances(analysis['identifier'])
        analysis_id = uuid4().__str__()
        command = CreateAnalysisCommand(project_id, analysis_id)
        self.command_bus.execute(command)
        command = ProcessRestaurantOverviewCommand(project_id, analysis_id)
        self.command_bus.execute(command)
        command = ProcessRestaurantReviewsCommand(project_id)
        self.command_bus.execute(command)

    def check_analysis_exists(self, project_id):
        query = GetAnalysisOfProjectQuery(project_id)
        return self.query_bus.execute(query)

    def remove_previous_instances(self, analysis_id):
        command = RemoveAnalysisCommand(analysis_id)
        self.command_bus.execute(command)

    def add_keywords(self):
        add_more = True
        while add_more:
            word = input('Keyword: ')
            if word == '':
                add_more = False
            else:
                command = CreateKeywordCommand(word)
                try:
                    self.command_bus.execute(command)
                except KeywordAlreadyCreatedException:
                    print('Keyword already exists')

    def show_projects(self):
        query = GetProjectsQuery()
        projects = self.query_bus.execute(query)
        index = 1
        for project in projects:
            self.projects[index] = project['identifier']
            print('%d. %s' % (index, project['name']))
            index += 1
        return input('Select project: ')

    def synonyms(self):
        repository = self.dependency_injector.get('app.repository.synonyms')
        print(repository.get_all())

    def show_analysis(self, project_id):
        query = GetProjectOfIdQuery(project_id)
        project = self.query_bus.execute(query)
        query = GetAnalysisOfIdQuery(project['analysis_id'])
        analysis = self.query_bus.execute(query)

        headers = ['Word', 'Karma', 'Appearances']
        data = []
        for keyword in analysis['key_points']:
            data.append([
                keyword['identifier'],
                keyword['karma'],
                len(keyword['appearances'])
            ])

        print(project['name'].upper())
        print('====================================')
        print('Karma: %s' % analysis['karma'])
        print(tabulate(data, headers))

    def load_countries(self):
        with open('./src/application/data/country.json', 'r') as file:
            read_data = file.read()
        print(read_data)
        countries = json.loads(read_data)
        for key, country in countries.items():
            command = CreateCountryCommand(key, country)
            self.command_bus.execute(command)

    def load_keywords(self):
        service = self.dependency_injector.get('app.fixtures.keyword_loader')
        service.execute()


def run_main():
    """
    Run application
    """
    operation = None
    main = Main()
    main.dependency_injector.list()

    print('\n\n')
    while operation != 9:
        operation = int(main.request_operation())
        if operation == 1:
            project_id = uuid4().__str__()
            name = main.request_project_name()
            main.create_project(project_id, name)
        elif operation == 2:
            project_number = int(main.show_projects())
            main.download_social_data(main.projects[project_number])
        elif operation == 3:
            project_number = int(main.show_projects())
            main.analyze_project(main.projects[project_number])
        elif operation == 4:
            main.add_keywords()
        elif operation == 5:
            main.synonyms()
        elif operation == 6:
            index = int(main.show_projects())
            main.show_analysis(main.projects[index])
        elif operation == 7:
            main.load_countries()
        elif operation == 8:
            main.load_keywords()


if __name__ == '__main__':
    run_main()
