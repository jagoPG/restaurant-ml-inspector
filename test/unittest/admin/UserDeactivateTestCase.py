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


class UserDeactivateTestCase(AppTestCase):
    def test_user_deactivation(self):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.do_xhr_put(
            '/admin/user/deactivate/%s/' % 'client'
        )
        self.assertEqual(response.status_code, 200)

    def test_no_xhr_request(self):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.client.put(
            '/admin/user/deactivate/%s/' % 'client'
        )
        self.assertEqual(response.status_code, 400)

    def test_no_existing_user(self):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.do_xhr_put(
            '/admin/user/deactivate/%s/' % 'rofl'
        )
        self.assertEqual(response.status_code, 404)

    def test_no_admin_permission(self):
        with self.client.session_transaction() as session:
            self.set_up_client_session(session)
        response = self.do_xhr_put(
            '/admin/user/activate/%s/' % 'client'
        )
        self.assertEqual(response.status_code, 403)
