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

import json

from test.unittest.AppTestCase import AppTestCase


class GetUsersTestCase(AppTestCase):
    def test_get_users(self):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.do_xhr_get('/admin/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreaterEqual(len(data), 2)

    def test_get_projects_no_xhr(self):
        response = self.client.get('/admin/users/')
        self.assertEqual(response.status_code, 400)

    def test_get_projects_no_admin(self):
        with self.client.session_transaction() as session:
            session['user_email'] = 'client@example.com'
            session['user_roles'] = '[\'DEVELOPER\', \'BUSINESSMAN\']'
            session['user_identifier'] = 'client'
        response = self.do_xhr_get('/admin/users/')
        self.assertEqual(response.status_code, 403)
