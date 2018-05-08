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

import unittest
import warnings
from flask import json
from web.core import app


class AppTestCase(unittest.TestCase):
    """
    Shared test case of Admin side
    """

    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        app.testing = True
        self.client = app.test_client()

    @staticmethod
    def set_up_admin_session(session):
        session['google_token'] = ''
        session['user_email'] = 'admin@example.com'
        session['user_roles'] = '[\'ADMIN\']'
        session['user_identifier'] = 'admin'

    @staticmethod
    def set_up_client_session(session):
        session['google_token'] = ''
        session['user_email'] = 'client@example.com'
        session['user_roles'] = '[\'BUSINESSMAN\', \'DEVELOPER\']'
        session['user_identifier'] = 'client'

    def do_xhr_get(self, end_point):
        return self.client.get(
            end_point,
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )

    def do_xhr_delete(self, end_point):
        return self.client.delete(
            end_point,
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )

    def do_xhr_put(self, end_point, args=None):
        if args is None:
            args = {}
        return self.client.put(
            end_point,
            headers={'X-Requested-With': 'XMLHttpRequest'},
            data=json.dumps(args)
        )

    def do_xhr_post(self, end_point, args=None):
        if args is None:
            args = {}
        return self.client.post(
            end_point,
            headers={'X-Requested-With': 'XMLHttpRequest'},
            data=json.dumps(args)
        )
