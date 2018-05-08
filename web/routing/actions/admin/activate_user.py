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

from flask import current_app as app
from flask_mail import Message
from werkzeug.exceptions import NotFound

from src.application.command.user.activate_user import ActivateUserCommand
from src.application.query.user.get_user import GetUserQuery
from src.domain.exception import UserDoesNotExist
from web.routing.actions.action import Action


class ActivateUser(Action):
    def __init__(self):
        self.command_bus = None
        self.query_bus = None

    def invoke(self, request=None, **args):
        user_id = args['user_id']
        command = ActivateUserCommand(user_id)
        try:
            self.command_bus.execute(command)
            user = self.query_bus.execute(GetUserQuery(user_id))
            # self.__notify_user_activated(
            #     user['email'], user['name'], user['surnames'], user['roles']
            # )
        except UserDoesNotExist:
            raise NotFound
        return app.response_class(status=200)

    def __notify_user_activated(self, user_email, name, surnames, roles):
        mailer = app.config['email']
        roles = ''.join([role for role in roles])
        body = 'Dear {0} {1}, your account has been activated with the role {2}.' \
            .format(name, surnames, roles)
        message = Message(
            body=body,
            subject='Restaurant Reviews | Your account has been activated',
            sender=app.config['MAIL_USERNAME'],
            recipients=[user_email],
        )
        mailer.send(message)
