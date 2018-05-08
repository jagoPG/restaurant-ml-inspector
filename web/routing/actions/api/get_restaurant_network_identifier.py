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

from flask import current_app, json
from werkzeug.exceptions import BadRequest, NotFound

from src.application.query.data_sources.retrieve_facebook_id import \
    RetrieveFacebookIdQuery
from src.application.query.data_sources.retrieve_google_places_id import \
    RetrieveGooglePlacesIdQuery
from src.domain.exception import RestaurantNotFoundInGooglePlaces, \
    RestaurantNotFoundInFacebook, RestaurantNotFoundInTwitter
from src.social_networks.facebook import FacebookException
from web.routing.actions.action import Action


class GetRestaurantNetworkIdentifier(Action):
    def __init__(self):
        self.query_bus = None

    def invoke(self, request=None, **kwargs):
        place_name = request.args['name']
        network_name = request.args['network']

        self.__check_not_null_field(request.args, 'name')
        self.__check_not_null_field(request.args, 'network')

        if place_name.strip() == '':
            raise BadRequest
        if network_name == 'Facebook':
            self.__check_not_null_field(request.args, 'country')
            query = RetrieveFacebookIdQuery(place_name, request.args['country'])
        elif network_name == 'Google Places':
            self.__check_not_null_field(request.args, 'country')
            query = RetrieveGooglePlacesIdQuery(
                place_name,
                request.args['country']
            )
        else:
            current_app.logger.warning(
                '%s social network account does not exist at %s' % (
                    place_name, network_name
                ))
            raise NotFound
        try:
            response = self.query_bus.execute(query)
        except (
                RestaurantNotFoundInGooglePlaces, RestaurantNotFoundInFacebook,
                RestaurantNotFoundInTwitter
        ):
            raise NotFound
        except FacebookException:
            return current_app.response_class(status=400, response=json.dumps({
                'error': 'Facebook API is not available'
            }))
        return current_app.response_class(
            status=200, response=json.dumps(response)
        )

    @staticmethod
    def __check_not_null_field(dictionary, field):
        if dictionary[field].strip() == '':
            raise BadRequest
