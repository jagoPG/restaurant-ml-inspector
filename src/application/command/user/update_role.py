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

from src.domain.exception import UserDoesNotExist
from src.domain.model import User
from src.infrastructure.command_bus import CommandHandler
from uuid import uuid4


class UpdateUserRoleCommand(object):
    """
    Changes the user role of an user
    """

    def __init__(self, user_identifier, roles):
        self.user_identifier = user_identifier
        self.roles = roles


class UpdateUserRole(CommandHandler):
    def __init__(self):
        self.user_repository = None

    def invoke(self, command):
        user = self.__get_user(command.user_identifier)
        self.__manage_roles(user, command.roles)

    def __get_user(self, user_id):
        user = self.user_repository.get_of_identifier(user_id)
        if not user:
            raise UserDoesNotExist
        return user

    def __manage_roles(self, user, roles):
        for role in User.get_roles():
            if role not in roles:
                user.revoke_role(role)
            else:
                user.grant_role(role)
                if role == 'DEVELOPER':
                    self.__generate_api_key(user)
        self.user_repository.persist(user)

    @staticmethod
    def __generate_api_key(user):
        user.api_key = uuid4().__str__()
