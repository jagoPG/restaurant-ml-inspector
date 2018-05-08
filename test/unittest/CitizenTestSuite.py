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
from flask import json
import warnings
from web.core import app


class CitizenTestSuite(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        app.testing = True
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_near_restaurant(self):
        response = self.client.get(
            '/api/restaurant/nearby/?latitude=%f&longitude=%f' %
            (43.296483, -2.989619),
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreaterEqual(len(data), 1)

    def test_get_no_near_restaurant(self):
        response = self.client.get(
            '/api/restaurant/nearby/?latitude=%f&longitude=%f' %
            (41.761497, -30.967533),
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])

    def test_bad_request_args_near_restaurant(self):
        response = self.client.get(
            '/api/restaurant/nearby/',
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 400)

    def test_bad_request_headers_near_restaurant(self):
        response = self.client.get(
            '/api/restaurant/nearby/?latitude=%f&longitude=%f' %
            (41.761497, -30.967533),
        )
        self.assertEqual(response.status_code, 400)
