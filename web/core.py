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

from flask import Flask, send_from_directory, session
from flask_oauthlib.client import OAuth
from flask_mail import Mail
from logging.handlers import SMTPHandler
from neomodel import config
from src.application.config import NEO4J_CONFIG, GOOGLE_OAUTH_ID, GOOGLE_OAUTH_SECRET
from src.infrastructure.dependency_injector import DependencyInjector
from web.routing.admin import admin_page
from web.routing.client import client_page
from web.routing.api import api_page
from web.routing.user_authentication import user_authentication
import logging
import os


def download_dependencies():
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')


def setup_database():
    if os.environ['DEBUG'] == 'True':
        config.DATABASE_URL = 'bolt://%s:%s@localhost:7687' % (NEO4J_CONFIG['user'], NEO4J_CONFIG['passwd'])
    else:
        BOLT_URL = os.environ['GRAPHENEDB_BOLT_URL']
        BOLT_USER = os.environ['GRAPHENEDB_BOLT_USER']
        BOLT_PASSWORD = os.environ['GRAPHENEDB_BOLT_PASSWORD']
        config.DATABASE_URL = 'bolt://%s:%s@%s' % (BOLT_USER, BOLT_PASSWORD, BOLT_URL[BOLT_URL.find('//') + 2:])


def setup_email(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = '465'
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
    app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
    mail = Mail(app)
    app.config['email'] = mail


def setup_logging(app):
    # Set up Flask logging
    app.config['PROPAGATE_EXCEPTIONS'] = True
    formatter = logging.Formatter(
        '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    app.logger.addHandler(stream_handler)
    if os.environ['DEBUG'] == 'True':
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.WARNING)
    # mail_handler = SMTPHandler(
    #     mailhost='smtp',
    #     fromaddr=app.config['MAIL_USERNAME'],
    #     credentials=app.config['MAIL_PASSWORD'],
    #     toaddrs='jagobapg@protonmail.com',
    #     subject='[FATAL ERROR] Restaurant Review App'
    # )
    # mail_handler.setFormatter(formatter)
    # mail_handler.setLevel(logging.CRITICAL)
    # app.logger.addHandler(mail_handler)

    # Set up Python logging
    logging.basicConfig(
        format='%(levelname)s:%(message)s',
        level=logging.ERROR
    )


def setup_google_oauth(app):
    app.config['GOOGLE_ID'] = GOOGLE_OAUTH_ID
    app.config['GOOGLE_SECRET'] = GOOGLE_OAUTH_SECRET
    oauth = OAuth(app)
    google = oauth.remote_app(
        'google',
        consumer_key=app.config.get('GOOGLE_ID'),
        consumer_secret=app.config.get('GOOGLE_SECRET'),
        request_token_params={
            'scope': 'email'
        },
        base_url='https://www.googleapis.com/oauth2/v1/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
    )
    app.config['GOOGLE'] = google
    return google


def register_blueprints(app):
    app.register_blueprint(admin_page, url_prefix='/admin')
    app.register_blueprint(client_page, url_prefix='/')
    app.register_blueprint(api_page, url_prefix='/api')
    app.register_blueprint(user_authentication, url_prefix='/auth')


def load_basic_data(app):
    dependency_injector = app.config['dependency_injector']
    loader = dependency_injector.get('app.fixtures.basic_structure_loader')
    loader.execute()


# Initialise database and application
setup_database()
download_dependencies()
app = Flask(__name__)
app.secret_key = os.environ['SECRET']
setup_logging(app)
setup_email(app)
google = setup_google_oauth(app)
register_blueprints(app)
app.config['dependency_injector'] = DependencyInjector()
load_basic_data(app)


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


# General requests
@app.route('/static/<path:path>')
def get_static(path):
    return send_from_directory('js', path)


@app.route('/images/<path:path>')
def get_images(path):
    return send_from_directory('static/images', path)


@app.route('/file/<path:path>')
def get_file(path):
    return send_from_directory('static/files', path)
