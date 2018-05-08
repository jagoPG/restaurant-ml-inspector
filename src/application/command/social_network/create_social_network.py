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

from src.domain.model import SocialNetwork
from src.infrastructure.command_bus import CommandHandler


class CreateSocialNetworkCommand(object):
    """
    Creates default Social Networks Handler
    """

    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier


class CreateSocialNetwork(CommandHandler):
    def __init__(self):
        self.social_networks_repository = None

    def invoke(self, command):
        if not self.__is_social_network_node_created(command.name):
            self.__create_social_network_node(command.name, command.identifier)

    def __is_social_network_node_created(self, name):
        try:
            self.social_networks_repository.get_of_name(name)
        except SocialNetwork.DoesNotExist:
            return False
        return True

    def __create_social_network_node(self, name, identifier):
        social_network = SocialNetwork(
            name=name,
            identifier=identifier
        )
        self.social_networks_repository.persist(social_network)
