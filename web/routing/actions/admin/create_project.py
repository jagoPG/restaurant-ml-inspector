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
from flask import session, current_app as app
from werkzeug.exceptions import BadRequest
from src.application.command.project.create_project import CreateProjectCommand
from web.routing.actions.action import Action


class CreateProject(Action):
    def __init__(self):
        self.command_bus = None

    def invoke(self, request=None, **kwargs):
        json_data = kwargs['json_data']

        if json_data['name'] == '':
            raise BadRequest
        command = CreateProjectCommand(
            uuid4().__str__(), json_data['name'], json_data['description'],
            session['user_identifier']
        )
        self.command_bus.execute(command)

        return app.response_class(status=201)
