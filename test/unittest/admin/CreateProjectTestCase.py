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

from test.unittest.AppTestCase import AppTestCase
from json import dumps


class CreateProjectTestCase(AppTestCase):
    CORRECT_POST_DATA = {
        'name': 'Mi prueba chachi',
        'description': ''
    }
    INCORRECT_POST_DATA = {
        'name': '',
        'description': ''
    }

    def test_no_logged_in(self):
        response = self.do_xhr_post(
            '/admin/project/',
            args=CreateProjectTestCase.CORRECT_POST_DATA
        )
        self.assertEqual(response.status_code, 403)

    def test_no_xhr(self):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.client.post(
            '/admin/project/',
            data=dumps(CreateProjectTestCase.CORRECT_POST_DATA)
        )
        self.assertEqual(response.status_code, 400)

    def test_wrong_parameters(self):
        with self.client.session_transaction() as session:
            self.set_up_client_session(session)
        response = self.do_xhr_post(
            '/admin/project/',
            args=CreateProjectTestCase.INCORRECT_POST_DATA
        )
        self.assertEqual(response.status_code, 400)
