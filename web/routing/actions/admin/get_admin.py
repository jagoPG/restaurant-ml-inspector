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

from flask import session, render_template, redirect

from web.routing.actions.action import Action


class GetAdmin(Action):
    def invoke(self, request=None, **kwargs):
        if 'google_token' in session:
            return render_template(
                'index.html',
                user_email=session['user_email'],
                user_roles=','.join([item for item in session['user_roles']])
            )
        else:
            return redirect('/auth/')
