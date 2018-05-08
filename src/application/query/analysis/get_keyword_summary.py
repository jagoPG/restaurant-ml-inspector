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

from src.domain.exception import ProjectDoesNotExist
from src.infrastructure.query_bus import QueryHandler


class GetKeywordSummaryQuery(object):
    def __init__(self, project_id):
        self.project_id = project_id


class GetKeywordSummary(QueryHandler):
    SERVICE_KEYWORDS = [
        '79fd76ae-67c4-4d43-bbfe-19a710af1adf',
        'ab637ef8-419d-46c4-b479-1f682df18b05'
    ]
    PRICE_KEYWORDS = [
        '61248ae5-e624-4cfb-a304-2b8678d5922c'
    ]
    LOCATION_KEYWORDS = [
        'b7c99e94-3dca-43de-b08a-b465b9c31112',
        '9ab33c8b-98b0-4c91-b2f5-040c69771743'
    ]
    FOOD_KEYWORDS = [
        '8880f641-d560-41d8-a8bd-64951b249b04',
        '25699329-e8a9-4c43-9ce3-4df36224858e',
        'eb2db5f4-8847-45ec-919f-d900a3e26d33',
        'f4c866cf-e092-427d-8604-dfb5d844c2f5',
        '721fb226-9169-46db-9cdb-97467111fa65',
        'ca1b2639-c543-4d1a-a406-807992c2592e',
        '69353b54-a237-4a27-bb07-aed371d325d3',
        '6414509f-6cad-4804-a246-d2aafa8e59d7',
        'b4f388ce-2439-41e9-937e-d1ed505872fc'
    ]

    def __init__(self):
        self.project_repository = None
        self.synonym_repository = None
        self._service_score = 0
        self._price_score = 0
        self._location_score = 0
        self._food_score = 0
        self._total_score = 0

    def invoke(self, query):
        project = self.__check_project_exists(query.project_id)
        self.__gather_keyword_scores(project)
        return self.__transform_summary_data()

    def __check_project_exists(self, project_id):
        project = self.project_repository.get_of_id(project_id)
        if project is None:
            raise ProjectDoesNotExist()
        return project

    def __gather_keyword_scores(self, project):
        keypoints = project.get_analysis().get_key_points()
        self._service_score = self.__gather_scores(
            GetKeywordSummary.SERVICE_KEYWORDS, keypoints
        )
        self._food_score = self.__gather_scores(
            GetKeywordSummary.FOOD_KEYWORDS, keypoints
        )
        self._price_score = self.__gather_scores(
            GetKeywordSummary.PRICE_KEYWORDS, keypoints
        )
        self._location_score = self.__gather_scores(
            GetKeywordSummary.LOCATION_KEYWORDS, keypoints
        )
        self.__calculate_total()

    def __calculate_total(self):
        score = 0
        items = 0

        if self._service_score:
            score = self._service_score
            items += 1
        if self._food_score:
            score = score + self._food_score
            items += 1
        if self._location_score:
            score = score + self._location_score
            items += 1
        if self._price_score:
            score = score + self._price_score
            items += 1
        if items == 0:
            self._total_score = None
        else:
            self._total_score = round(score / items, 3)

    def __gather_scores(self, synonym_ids, project_keywords):
        score = None
        for synonym_id in synonym_ids:
            keywords = self.synonym_repository.get_synonym_group(
                synonym_id, 'es'
            )
            for project_keyword in project_keywords:
                is_keyword = self.__is_keyword_in_synonym_group(
                    project_keyword, keywords
                )
                if not is_keyword:
                    continue
                if score is None:
                    score = project_keyword.karma
                else:
                    score = (score + project_keyword.karma) / 2
        return score

    @staticmethod
    def __is_keyword_in_synonym_group(project_keyword, keywords):
        for keyword in keywords:
            # Not all words are translated
            if keyword is None:
                continue
            if keyword.word == project_keyword.identifier:
                return True
        return False

    def __transform_summary_data(self):
        return {
            'service': self._service_score,
            'price': self._price_score,
            'location': self._location_score,
            'food': self._food_score,
            'total': self._total_score
        }
