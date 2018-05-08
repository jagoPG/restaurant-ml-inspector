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

import warnings

from test.unittest.AppTestCase import AppTestCase
from web.core import app


class GetProjectTestCase(AppTestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        app.testing = True
        self.client = app.test_client()

    def test_no_logged_in(self):
        response = self.do_xhr_get(
            '/api/project/%s/' % 'f886388e-8f38-4463-8e72-f725c3218379'
        )
        self.assertEqual(response.status_code, 403)

    def test_no_xhr(self):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.client.get(
            '/api/project/%s/' % 'f886388e-8f38-4463-8e72-f725c3218379',
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 400)

    def test_project_does_not_exists(self):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.do_xhr_get(
            '/api/project/%s/' % '1'
        )
        self.assertEqual(response.status_code, 404)

    def test_permission_denied(self):
        with self.client.session_transaction() as session:
            self.set_up_client_session(session)
        response = self.do_xhr_get(
            '/api/project/%s/' % 'f886388e-8f38-4463-8e72-f725c3218379'
        )
        self.assertEqual(response.status_code, 403)

    def test_admin_permission_in_client_project(self):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.do_xhr_get(
            '/api/project/%s/' % 'f1d6328e-8f98-2163-8e12-f7a523218379'
        )
        self.assertEqual(response.status_code, 403)
