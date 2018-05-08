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

from src.infrastructure.data_transformer import DataTransformer


class UserDataTransformer(DataTransformer):
    def read(self):
        user_data = {
            'identifier': str(self.instance.identifier),
            'name': self.instance.name,
            'surnames': self.instance.surnames,
            'roles': self.instance.roles,
            'is_verified': self.instance.is_verified,
            'email': self.instance.email
        }
        if self.instance.last_login:
            user_data['last_access'] = self.instance.last_login.strftime(
                '%Y-%m-%d %H:%M:%S'
            )
        return user_data
