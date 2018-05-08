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

from src.application import config
from tabulate import tabulate
from xml.dom import minidom


class DependencyResolver(object):
    """
    The Dependency Resolver is a manager of micro-services. When the
    application is loaded, the XML files specified are read in order to store
    the services in memory. After initialising, the services can be retrieved
    through the :func:`get_service`
    """
    services = {}

    def __init__(self):
        self.__load_configuration_files([
            'src/infrastructure/services/buses.xml',
            'src/infrastructure/services/repositories.xml',
            'src/infrastructure/services/data_transformer.xml',
            'src/infrastructure/services/social_network_clients.xml',
            'src/infrastructure/services/analysis.xml',
            'src/infrastructure/services/commands.xml',
            'src/infrastructure/services/queries.xml',
            'src/infrastructure/services/fixtures.xml',
            'src/infrastructure/services/action.xml',
        ])

    def __load_configuration_files(self, files_names):
        for file_name in files_names:
            self.__parse_xml_file(file_name)

    def __parse_xml_file(self, file_name):
        with open(file_name, mode='r', encoding='utf-8') as xml:
            document = minidom.parse(xml)
            for service in document.documentElement.getElementsByTagName('service'):
                self.__parse_xml_service(service)

    def __parse_xml_service(self, xml_node):
        args = {}
        identifier = xml_node.getAttribute('id')
        full_path = xml_node.getAttribute('class')
        class_name, module_name = self.__separate_class_and_module(full_path)

        # Extract arguments from service
        arguments = xml_node.getElementsByTagName('arguments')
        if arguments:
            for argument in arguments[0].getElementsByTagName('argument'):
                name = argument.getAttribute('name')
                kind = argument.getAttribute('type')
                value = self.__extract_argument_value(argument.firstChild.nodeValue, kind)
                args[name] = value
        service = self.__store_service(identifier, module_name, class_name, args)

        # After store the service, register the service to be managed by other
        # service
        tags = xml_node.getElementsByTagName('tags')
        if tags:
            self.__handle_tags(tags[0].getElementsByTagName('tag'), service)

    @staticmethod
    def __separate_class_and_module(full_path):
        last_separator_char = full_path.rfind('.')
        class_name = full_path[last_separator_char + 1:]
        module_name = full_path[:last_separator_char]
        return class_name, module_name

    def __handle_tags(self, tags, service):
        for tag in tags:
            name = handles = None
            if tag.hasAttribute('name'):
                name = tag.getAttribute('name')
            if tag.hasAttribute('handles'):
                handles = tag.getAttribute('handles')
            if name and handles:
                parent_service = self.get_service(name)
                parent_service.record(handles, service)

    def __extract_argument_value(self, argument, kind):
        if kind == 'config':
            return vars(globals()['config'])[argument]
        elif kind == 'service':
            return self.get_service(argument)
        elif kind == 'file':
            return argument

    def __store_service(self, identifier, module_name, class_name, args=None):
        if identifier in self.services:
            raise DependencyIdentifierDuplicated()
        instance = DependencyResolver.__get_class(module_name, class_name)()
        for arg in args:
            instance.set_argument(arg, args[arg])
        if DependencyResolver.__requires_initialisation(instance):
            instance.initialise()
        self.services[identifier] = instance

        return instance

    @staticmethod
    def __requires_initialisation(instance):
        method = getattr(instance, 'initialise', None)
        return callable(method)

    @staticmethod
    def __get_class(module_name, class_name):
        parts = module_name.split('.')
        module_reference = __import__(module_name)
        parts.append(class_name)
        for folder in parts[1:]:
            module_reference = getattr(module_reference, folder)
        return module_reference

    def get_service(self, identifier):
        """
        Retrieves a service with an identifier

        :param identifier: Identifier of the service
        :type identifier: - string
        :return: A service
        """
        if identifier not in self.services:
            raise DependencyNotFound(identifier)
        return self.services[identifier]

    def list_services(self):
        """
        Print a list of the available services
        """
        data = []
        headers = ['Identifier', 'Class Path']
        for service in self.services:
            item = []
            instance = self.services[service]
            item.append(service)
            item.append('%s.%s' % (instance.__module__, instance.__class__.__name__))
            data.append(item)
        print(tabulate(data, headers))


class DependencyInjector(object):
    """
    This class is used for hide the :class:`DependencyResolver`. Just acts as
    façade
    """

    def __init__(self):
        self.resolver = DependencyResolver()

    def get(self, identifier):
        """
        Retrieves a service from the resolver
        """
        return self.resolver.get_service(identifier)

    def list(self):
        """
        Print a list of the available services
        """
        return self.resolver.list_services()


class Dependency(object):
    """
    A dependency is a class instance that is wanted to be managed by the :class:`DependencyResolver`.
    """

    def set_argument(self, identifier, value):
        """
        Sets a value to the variable with an identifier

        :param identifier: The identifier of the dependency
        :param value: The instance that want to be referenced from the service
        :type identifier: string
        :type value: mixed
        """
        if identifier in vars(self):
            vars(self)[identifier] = value

    def initialise(self):
        """
        Methods that want to be run after the arguments have been set
        """


class DependencyNotFound(Exception):
    """
    Dependency does not exist
    """


class InvalidArgumentType(Exception):
    """
    The argument type defined in the XML file is invalid
    """


class DependencyIdentifierDuplicated(Exception):
    """
    The identifier of the service is duplicated
    """
