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

from test.unittest.admin.AnalyseProjectTestCase import AnalyseProjectTestCase
from test.unittest.admin.CreateProjectSourcesTestCase import \
    CreateProjectSourcesTestCase

from test.unittest.admin.CreateProjectTestCase import CreateProjectTestCase
from test.unittest.admin.DeleteProjectTestCase import DeleteProjectTestCase
from test.unittest.admin.EditProjectSourcesTestCase import \
    EditProjectSourcesTestCase
from test.unittest.admin.EditProjectTestCase import EditProjectTestCase
from test.unittest.admin.GetUsersTestCase import GetUsersTestCase
from test.unittest.admin.GrantUserRoleTestCase import GrantUserRoleTestCase
from test.unittest.admin.MarkAsSpamTestCase import MarkAsSpamTestCase
from test.unittest.admin.RetrieveDataTestCase import RetrieveDataTestCase
from test.unittest.admin.SetReviewSentimentTestCase import \
    SetReviewSentimentTestCase
from test.unittest.admin.UserActivateTestCase import UserActivateTestCase
from test.unittest.admin.UserDeactivateTestCase import UserDeactivateTestCase
from test.unittest.CitizenTestSuite import CitizenTestSuite
from test.unittest.admin.GetProjectsTestCase import GetProjectsTestCase
from test.unittest.admin.HappyPathTestCase import HappyPathTestCase
from test.unittest.admin.IndexTestCase import TestAdminIndexCase


def set_up_citizen_test(suite):
    """
    Sets up citizens view tests
    """
    suite.addTest(CitizenTestSuite('test_index'))
    suite.addTest(CitizenTestSuite('test_get_near_restaurant'))
    suite.addTest(CitizenTestSuite('test_get_no_near_restaurant'))
    suite.addTest(CitizenTestSuite('test_bad_request_args_near_restaurant'))
    suite.addTest(CitizenTestSuite('test_bad_request_headers_near_restaurant'))


def set_up_admin_test(suite):
    """
    Sets up admin side tests
    """
    suite.addTest(EditProjectSourcesTestCase('test_no_xhr'))
    suite.addTest(EditProjectSourcesTestCase('test_no_log_in'))
    suite.addTest(EditProjectSourcesTestCase('test_no_edit_permission'))
    suite.addTest(EditProjectSourcesTestCase('test_no_fields'))

    suite.addTest(RetrieveDataTestCase('test_no_xhr'))
    suite.addTest(RetrieveDataTestCase('test_project_does_not_exist'))
    suite.addTest(RetrieveDataTestCase('test_no_user_permission'))

    suite.addTest(AnalyseProjectTestCase('test_no_xhr'))
    suite.addTest(AnalyseProjectTestCase('test_project_does_not_exist'))
    suite.addTest(AnalyseProjectTestCase('test_no_user_permission'))

    suite.addTest(MarkAsSpamTestCase('test_is_xhr'))
    suite.addTest(MarkAsSpamTestCase('test_user_has_permission'))
    suite.addTest(MarkAsSpamTestCase('test_resources_does_not_exist'))

    suite.addTest(SetReviewSentimentTestCase('test_is_xhr'))
    suite.addTest(SetReviewSentimentTestCase('test_user_has_permission'))
    suite.addTest(SetReviewSentimentTestCase('test_resources_does_not_exist'))

    suite.addTest(CreateProjectSourcesTestCase('test_no_xhr'))
    suite.addTest(CreateProjectSourcesTestCase('test_no_log_in'))
    suite.addTest(CreateProjectSourcesTestCase('test_no_edit_permission'))
    suite.addTest(CreateProjectSourcesTestCase('test_no_fields'))

    suite.addTest(GetProjectsTestCase('test_get_projects'))
    suite.addTest(GetProjectsTestCase('test_get_projects_no_xhr'))
    suite.addTest(GetProjectsTestCase('test_get_projects_no_logged'))

    suite.addTest(CreateProjectTestCase('test_no_logged_in'))
    suite.addTest(CreateProjectTestCase('test_no_xhr'))
    suite.addTest(CreateProjectTestCase('test_wrong_parameters'))

    suite.addTest(DeleteProjectTestCase('test_no_xhr'))
    suite.addTest(DeleteProjectTestCase('test_not_logged_in'))
    suite.addTest(DeleteProjectTestCase('test_no_permission'))
    suite.addTest(DeleteProjectTestCase('test_no_existing_project'))

    suite.addTest(EditProjectTestCase('test_no_xhr'))
    suite.addTest(EditProjectTestCase('test_no_args'))
    suite.addTest(EditProjectTestCase('test_wrong_args'))
    suite.addTest(EditProjectTestCase('test_no_logged_in'))
    suite.addTest(EditProjectTestCase('test_no_existing_project'))

    suite.addTest(TestAdminIndexCase('test_admin_index'))
    suite.addTest(TestAdminIndexCase('test_admin_index_no_log_in'))

    suite.addTest(GetUsersTestCase('test_get_users'))
    suite.addTest(GetUsersTestCase('test_get_projects_no_admin'))

    suite.addTest(UserDeactivateTestCase('test_no_admin_permission'))
    suite.addTest(UserDeactivateTestCase('test_user_deactivation'))
    suite.addTest(UserDeactivateTestCase('test_no_existing_user'))

    suite.addTest(UserActivateTestCase('test_user_activation'))
    suite.addTest(UserActivateTestCase('test_no_existing_user'))
    suite.addTest(UserActivateTestCase('test_no_admin_permission'))

    suite.addTest(GrantUserRoleTestCase('test_grant_user_role'))
    suite.addTest(GrantUserRoleTestCase('test_no_xhr'))
    suite.addTest(GrantUserRoleTestCase('test_is_admin'))
    suite.addTest(GrantUserRoleTestCase('test_user_does_not_exist'))
    suite.addTest(GrantUserRoleTestCase('test_invalid_fields'))

    # suite.addTest(HappyPathTestCase('test_project'))


def before_tests(fixture_manager):
    fixture_manager.set_up()


def after_tests(fixture_manager):
    fixture_manager.tear_down()


if __name__ == '__main__':
    suite = unittest.TestSuite()
    set_up_citizen_test(suite)
    set_up_admin_test(suite)
    runner = unittest.TextTestRunner()
    runner.run(suite)
