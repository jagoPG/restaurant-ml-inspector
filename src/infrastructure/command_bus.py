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


class CommandBus(object):
    """
    Searches an appropriate handler for a command
    """

    def __init__(self):
        self.commands = {}

    def record(self, command_class, handler):
        """
        Records a command handler in the command bus

        :arg command_class: <module>.<class> full qualifier
        :arg handler: instance of the service which will handle the request
        :type command_class: string
        :type handler: instance
        """
        if command_class in self.commands:
            raise CommandHandlerAlreadyExists()
        self.commands[command_class] = handler

    def execute(self, command):
        """
        Searches a command handler and launches the command

        :arg command: a Command DTO class
        """
        module_name = command.__module__
        class_name = command.__class__.__name__
        handler = self.__check_handler_exists(
            '%s.%s' % (module_name, class_name)
        )
        handler.invoke(command)

    def __check_handler_exists(self, command_class):
        if command_class not in self.commands:
            raise CommandHandlerNotFound
        return self.commands[command_class]


class CommandHandler(Dependency):
    """
    Definition of the methods a command handler must implement
    """

    def invoke(self, command):
        """
        Executes the command
        :param command: Command DTO with data
        """
        raise NotImplementedError()


class CommandHandlerNotFound(Exception):
    """
    This exception has to be raised if a command handler is not found
    """


class CommandHandlerAlreadyExists(Exception):
    """
    A command handler has already be defined
    """
