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

from ml_algorithms.models import ModelTest


def select_option():
    print('1. Linear')
    print('2. Gaussian NB')
    print('3. SVR')
    print('4. Logistic Regression')
    print('5. K Neighbours Classifier')
    print('6. Decision Tree Classifier')
    print('7. SVC')
    print('8. Exit')
    return int(input('Your selection [1-8]:'))


def load_script(model_test, option):
    if option == 1:
        model_test.test_linear()
    elif option == 2:
        model_test.test_gaussian_nb()
    elif option == 3:
        model_test.test_svr()
    elif option == 4:
        model_test.test_logistic_regression()
    elif option == 5:
        model_test.test_knn_classifier()
    elif option == 6:
        model_test.test_decision_tree_classifier()
    elif option == 7:
        model_test.test_svc()


if __name__ == '__main__':
    option = 0
    model_test = ModelTest()
    model_test.prepare_data_set()
    while option != 8:
        option = select_option()
        load_script(model_test, option)
