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

import os

NEO4J_CONFIG = {
    'user': os.environ.get('NEO4J_USER'),
    'passwd': os.environ.get('NEO4J_PASSWD')
}

TWITTER_CONSUMER_KEY = os.environ.get('TW_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TW_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('TW_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TW_ACCESS_TOKEN_SECRET')

FACEBOOK_OAUTH_APP_ID = os.environ.get('FB_APP_ID')
FACEBOOK_OAUTH_APP_SERCRET = os.environ.get('FB_APP_SECRET')
FACEBOOK_OAUTH_PERMISSIONS = os.environ.get('FB_PERMISSIONS')
FACEBOOK_OAUTH_CLIENT_ACCESS_TOKEN = os.environ.get('FB_CLIENT_ACCESS_TOKEN')

GOOGLE_PLACES_API_KEY = os.environ.get('GG_API_KEY')
GOOGLE_OAUTH_ID = os.environ.get('GG_OAUTH_ID')
GOOGLE_OAUTH_SECRET = os.environ.get('GG_OAUTH_SECRET')
