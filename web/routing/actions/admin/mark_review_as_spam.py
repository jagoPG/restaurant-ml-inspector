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
from werkzeug.exceptions import Forbidden, NotFound

from src.application.command.review.mark_spam import MarkReviewSpamCommand
from src.domain.exception import ReviewDoesNotExist, AccessViolation
from web.routing.actions.action import Action


class MarkReviewAsSpam(Action):
    def __init__(self):
        self.command_bus = None

    def invoke(self, request=None, **kwargs):
        json_data = kwargs['json_data']
        review_id = kwargs['review_id']
        project_id = kwargs['project_id']

        command = MarkReviewSpamCommand(
            review_id, project_id, bool(json_data['is_spam'])
        )
        try:
            self.command_bus.execute(command)
        except ReviewDoesNotExist:
            current_app.logger.warning(
                '{0} non existing review tried to marked as spam'.format(
                    review_id)
            )
            raise NotFound
        except AccessViolation:
            current_app.logger.warning(
                'Attempt to mark {0} review as spam denied'.format(review_id)
            )
            raise Forbidden
        return current_app.response_class(status=200)
