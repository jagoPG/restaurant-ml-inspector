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
from src.persistence.database.neo4j_repository import \
    Neo4jProjectRepository


class HappyPathTestCase(AppTestCase):
    def test_project(self):
        self.step_create_project()
        project_repository = Neo4jProjectRepository()
        project = project_repository.get_of_name('Test project')
        self.step_edit_project(project.identifier)
        self.step_set_up_sources(project.identifier)
        self.step_edit_sources(project.identifier)
        self.step_analyse(project.identifier)
        self.step_delete_project(project.identifier)

    def step_create_project(self):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.do_xhr_post(
            '/admin/project/', args={
                'name': 'Test project', 'description': 'One test project'
            }
        )
        self.assertEqual(response.status_code, 201)

    def step_edit_project(self, project_id):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.do_xhr_put(
            '/admin/project/%s/' % project_id, args={
                'name': 'Test project', 'description': 'One edited test project'
            }
        )
        self.assertEqual(response.status_code, 200)

    def step_set_up_sources(self, project_id):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.do_xhr_post(
            '/admin/project/sources/%s/' % project_id, args={
                'social_network': 'Google Places',
                'country': 'ES',
                'restaurant_id': 'ChIJfd2iaSRQTg0RjnorB3o83Zw'
            }
        )
        self.assertEqual(response.status_code, 201)
        response = self.do_xhr_post(
            '/admin/project/sources/%s/' % project_id, args={
                'social_network': 'Facebook',
                'country': 'ES',
                'restaurant_id': '108687705819966'
            }
        )
        self.assertEqual(response.status_code, 201)
        response = self.do_xhr_post(
            '/admin/project/sources/%s/' % project_id, args={
                'social_network': 'Twitter',
                'geo_position': '43.2955458,-2.9936103,1km',
                'restaurant_id': '#Restaurante Etxanobe'
            }
        )
        self.assertEqual(response.status_code, 201)

    def step_edit_sources(self, project_id):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.do_xhr_put(
            '/admin/project/sources/%s/' % project_id, args={
                'social_network': 'Google Places',
                'country': 'ES',
                'restaurant_id': 'ChIJfd2iaSRQTg0RjnorB3o83Zw'
            }
        )
        self.assertEqual(response.status_code, 201)
        response = self.do_xhr_put(
            '/admin/project/sources/%s/' % project_id, args={
                'social_network': 'Facebook',
                'country': 'ES',
                'restaurant_id': '108687705819966'
            }
        )
        self.assertEqual(response.status_code, 201)
        response = self.do_xhr_put(
            '/admin/project/sources/%s/' % project_id, args={
                'social_network': 'Twitter',
                'geo_position': '43.2955458,-2.9936103,10km',
                'restaurant_id': '#Restaurante Etxanobe'
            }
        )
        self.assertEqual(response.status_code, 201)

    def step_analyse(self, project_id):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.do_xhr_put(
            '/admin/project/retrieve-data/%s/' % project_id
        )
        self.assertEqual(response.status_code, 200)
        response = self.do_xhr_put(
            '/admin/project/analyse/%s/' % project_id
        )
        self.assertEqual(response.status_code, 200)

    def step_delete_project(self, project_id):
        with self.client.session_transaction() as session:
            self.set_up_admin_session(session)
        response = self.client.delete(
            '/admin/project/%s/' % project_id,
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 200)
