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

from src.domain.exception import UserAlreadyExists
from src.domain.model import User
from src.infrastructure.command_bus import CommandHandler


class CreateUserCommand(object):
    """
    Creates a new user
    """

    def __init__(self, user_id, email, name, surnames):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.surnames = surnames


class CreateUser(CommandHandler):
    def __init__(self):
        self.user_repository = None

    def invoke(self, command):
        user_id = command.user_id
        self.__check_user_exists(user_id)
        self.__create_user(
            user_id, command.email, command.name, command.surnames
        )

    def __check_user_exists(self, user_id):
        user = self.user_repository.get_of_identifier(user_id)
        if user:
            raise UserAlreadyExists()

    def __create_user(self, user_id, email, name, surnames):
        user = User(
            identifier=user_id,
            email=email,
            name=name,
            surnames=surnames,
            is_verified=False,
            roles=['BUSINESSMAN']
        )
        self.user_repository.persist(user)
