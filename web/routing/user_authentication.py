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

from flask import request, render_template, Blueprint, session, jsonify, \
    redirect, url_for, current_app as app, json
from flask_mail import Message
from flask_oauthlib.client import OAuthException
from src.application.command.user.create_user import CreateUserCommand
from src.application.query.user.get_user import GetUserQuery
from src.domain.exception import UserAlreadyExists, UserDoesNotExist,\
    UserAccountNotActivated
import requests

user_authentication = Blueprint('auth', __name__, template_folder='templates')


@user_authentication.route('/')
def authentication_home():
    if 'google_token' in session:
        return redirect('/admin/')
    else:
        return render_template('login.html')


@user_authentication.route('/login/')
def login():
    google = app.config['GOOGLE']
    return google.authorize(callback=url_for('auth.authorized', _external=True))


@user_authentication.route('/register')
def register():
    google = app.config['GOOGLE']
    return google.authorize(callback=url_for('auth.registered', _external=True))


@user_authentication.route('/register/registered/')
def registered():
    google = app.config['GOOGLE']
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    response = jsonify(
        google.get('userinfo').data
    )
    data = json.loads(response.data)
    command_bus = __get_command_bus()
    command = CreateUserCommand(
        data['id'], data['email'], data['given_name'], data['family_name']
    )
    try:
        command_bus.execute(command)
        # __notify_admin_user_registered(
        #     data['email'], data['given_name'], data['family_name']
        # )
        del session['google_token']
    except UserAlreadyExists:
        message = 'This e-mail is already registered.'
        del session['google_token']
        return render_template('login.html', error=message)
    return render_template('login.html')


@user_authentication.route('/login/authorized/')
def authorized():
    google = app.config['GOOGLE']
    try:
        resp = google.authorized_response()
    except OAuthException:
        return redirect('/auth/')
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    response = jsonify(
        google.get('userinfo').data
    )
    data = json.loads(response.data)
    query_bus = __get_query_bus()
    query = GetUserQuery(data['id'])
    try:
        user_data = query_bus.execute(query)
        session['user_email'] = user_data['email']
        session['user_roles'] = user_data['roles']
        session['user_identifier'] = data['id']
        return redirect('/admin/')
    except UserDoesNotExist:
        message = """
            User account does not exist. Log out from your Google account if you
            want to try with other account.
        """
        del session['google_token']
    except UserAccountNotActivated:
        message = 'This account is not activated.'
        del session['google_token']
    return render_template('login.html', error=message)


@user_authentication.route('/logout/', methods=['GET'])
def logout():
    del session['user_email']
    del session['user_roles']
    del session['user_identifier']
    requests.post('https://accounts.google.com/o/oauth2/revoke',
                  params={'token': session['google_token'][0]},
                  headers={'content-type': 'application/x-www-form-urlencoded'})
    del session['google_token']
    return redirect('/auth/')


def __get_command_bus():
    dependency_injector = app.config['dependency_injector']
    return dependency_injector.get('app.command_bus')


def __get_query_bus():
    dependency_injector = app.config['dependency_injector']
    return dependency_injector.get('app.query_bus')


def __notify_admin_user_registered(user_email, name, surnames):
    mailer = app.config['email']
    message = Message(
        body='The user %s %s was registered with e-mail %s.' % (
            name, surnames, user_email
        ),
        subject='User registered @ Restaurant Reviews',
        sender=app.config['MAIL_USERNAME'],
        recipients=['jagobapg@protonmail.com'],
    )
    mailer.send(message)
