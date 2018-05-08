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


class MarkAsSpamTestCase(AppTestCase):
    CORRECT_ARGS = {
        'is_spam': True
    }

    def test_is_xhr(self):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.client.put(
            '/admin/project/%s/review/%s/spam/' % (
                'f886388e-8f38-4463-8e72-f725c3218379',
                '230390187297922_1713062622337830'
             ),
            data=dumps(MarkAsSpamTestCase.CORRECT_ARGS)
        )
        self.assertEquals(response.status_code, 400)

    def test_user_has_permission(self):
        with self.client.session_transaction() as session:
            self.set_up_client_session(session)
        response = self.do_xhr_put(
            '/admin/project/%s/review/%s/spam/' % (
                'f886388e-8f38-4463-8e72-f725c3218379',
                '230390187297922_1713062622337830'
            ),
            args=MarkAsSpamTestCase.CORRECT_ARGS
        )
        self.assertEquals(response.status_code, 403)

    def test_resources_does_not_exist(self):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.do_xhr_put(
            '/admin/project/%s/review/%s/spam/' % (
                '1',
                '1'
            ),
            args=MarkAsSpamTestCase.CORRECT_ARGS
        )
        self.assertEquals(response.status_code, 404)
        response = self.do_xhr_put(
            '/admin/project/%s/review/%s/spam/' % (
                'f886388e-8f38-4463-8e72-f725c3218379',
                '1'
            ),
            args=MarkAsSpamTestCase.CORRECT_ARGS
        )
        self.assertEquals(response.status_code, 404)
