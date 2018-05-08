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


class QueryBus(object):
    """
    Searches an appropriate Query Handler for a Query
    """

    def __init__(self):
        self.queries = {}

    def record(self, query_class, handler):
        """
        Records a command handler in the command bus

        :arg query_class: <module>.<class> full qualifier
        :arg handler: instance of the service which will handle the request
        :type query_class: string
        :type handler: instance
        """
        if query_class in self.queries:
            raise QueryHandlerAlreadyExists()
        self.queries[query_class] = handler

    def execute(self, query):
        """
        Searches a query handler, launches the query and returns the data

        :arg query: a Query DTO class
        """
        module_name = query.__module__
        class_name = query.__class__.__name__
        handler = self.__check_handler_exists(
            '%s.%s' % (module_name, class_name)
        )
        return handler.invoke(query)

    def __check_handler_exists(self, query_class):
        if query_class not in self.queries:
            raise QueryHandlerNotFound
        return self.queries[query_class]


class QueryHandler(Dependency):
    """
    Definition of the methods a query handler mus implement
    """

    def invoke(self, query):
        """
        Executes a query and returns the data
        :param query: Query DTO with the requirements
        :return: Data returned
        """


class QueryHandlerNotFound(Exception):
    """
    This exception is raised when a query handler is not found
    """


class QueryHandlerAlreadyExists(Exception):
    """
    A query handler has already be defined
    """
