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


class EditProjectTestCase(AppTestCase):
    CORRECT_POST_DATA = {
        'name': 'Mi prueba chachi',
        'description': ''
    }
    INCORRECT_POST_DATA = {
        'name': '',
        'description': ''
    }

    def test_no_xhr(self):
        response = self.client.put(
            '/admin/project/%s/' % 'f886388e-8f38-4463-8e72-f725c3218379',
            data=dumps(EditProjectTestCase.CORRECT_POST_DATA)
        )
        self.assertEqual(response.status_code, 400)

    def test_no_args(self):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.do_xhr_put(
            '/admin/project/%s/' % 'f886388e-8f38-4463-8e72-f725c3218379'
        )
        self.assertEqual(response.status_code, 400)

    def test_wrong_args(self):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.do_xhr_put(
            '/admin/project/%s/' % 'f886388e-8f38-4463-8e72-f725c3218379',
            args=EditProjectTestCase.INCORRECT_POST_DATA
        )
        self.assertEqual(response.status_code, 400)

    def test_no_logged_in(self):
        response = self.do_xhr_put(
            '/admin/project/%s/' % 'f886388e-8f38-4463-8e72-f725c3218379',
            args=dumps(EditProjectTestCase.CORRECT_POST_DATA)
        )
        self.assertEqual(response.status_code, 403)

    def test_no_existing_project(self):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.do_xhr_put(
            '/admin/project/%s/' % '1',
            args=EditProjectTestCase.INCORRECT_POST_DATA
        )
        self.assertEqual(response.status_code, 404)
