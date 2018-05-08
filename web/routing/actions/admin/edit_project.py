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

from flask import current_app
from werkzeug.exceptions import BadRequest

from src.application.command.project.edit_project import EditProjectCommand
from web.routing.actions.action import Action


class EditProject(Action):
    def __init__(self):
        self.command_bus = None

    def invoke(self, request=None, **kwargs):
        json_data = kwargs['json_data']
        project_id = kwargs['project_id']

        if json_data['name'] == '':
            raise BadRequest
        command = EditProjectCommand(
            project_id, json_data['name'], json_data['description']
        )
        self.command_bus.execute(command)

        return current_app.response_class(status=200)
