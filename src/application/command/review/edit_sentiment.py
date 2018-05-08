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

from src.domain.exception import ReviewDoesNotExist, AccessViolation
from src.infrastructure.command_bus import CommandHandler


class EditReviewSentimentCommand(object):
    """
    Sets a sentiment value to a review
    """
    def __init__(self, review_id, project_id, sentiment):
        self.review_id = review_id
        self.project_id = project_id
        self.sentiment = sentiment


class EditReviewSentiment(CommandHandler):
    def __init__(self):
        self.review_repository = None

    def invoke(self, command):
        review = self.__retrieve_review(command.review_id)
        self.__check_review_belongs_to_project(review, command.project_id)
        self.__check_sentiment_score(command.sentiment)
        review.sentiment = command.sentiment
        self.review_repository.persist(review)

    def __retrieve_review(self, review_id):
        review = self.review_repository.get_of_id(review_id)
        if not review:
            raise ReviewDoesNotExist
        return review

    @staticmethod
    def __check_review_belongs_to_project(review, project_id):
        if not review.is_from_project(project_id):
            raise AccessViolation

    @staticmethod
    def __check_sentiment_score(sentiment):
        if sentiment > 1 or sentiment < -1:
            raise ValueError
