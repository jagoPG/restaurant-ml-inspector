/**
 * Copyright 2017-2018 Jagoba Pérez-Gómez
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at

 * http://www.apache.org/licenses/LICENSE-2.0

 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import React, {Component} from 'react';
import Map from 'pigeon-maps';
import Overlay from 'pigeon-overlay';
import PropTypes from 'prop-types';
import {requestNearbyRestaurants} from './api';
import './MapItem.scss';

class MapItem extends Component {
  constructor(props) {
    super(props);
    this.subscribeToGeoLocation();
    this.state = {
      currentPosition: null,
      restaurants: [],
    };
  }

  refreshListOfRestaurants() {
    if (!this.state.currentPosition) {
      return;
    }
    const coords = this.state.currentPosition.coords;
    requestNearbyRestaurants({
      latitude: coords.latitude,
      longitude: coords.longitude
    }, this.onRestaurantRequested.bind(this))
  }

  onRestaurantRequested(response) {
    this.setState({restaurants: response});
  }

  subscribeToGeoLocation() {
    if (!navigator.geolocation.getCurrentPosition) {
      return;
    }
    navigator.geolocation.getCurrentPosition(this.updateUserPosition.bind(this));
  }

  updateUserPosition(position) {
    this.setState({
      currentPosition: position
    });
    if (!this.state.restaurants.length) {
      this.refreshListOfRestaurants();
    }
  }

  onMarkerClicked(evt) {
    const projectId = evt.currentTarget.dataset.payload;
    this.props.onRestaurantClicked(projectId);
  }

  getCurrentPositionMarker(latitude, longitude, isVisible) {
    let className = 'map_item__marker' + (isVisible ? '' : ' map_item__marker--hidden');
    return (
      <Overlay anchor={[latitude, longitude]}>
        <img src='/images/marker_person.png'
             className={className}/>
      </Overlay>
    );
  }

  render() {
    let latitude, longitude, overlays, currentPositionOverlay;
    const height = this.props.width * 0.7;

    if (this.state.currentPosition) {
      const coords = this.state.currentPosition.coords;
      latitude = coords.latitude;
      longitude = coords.longitude;
    } else {
      latitude = 43.2634271;
      longitude = -3.2137182;
    }
    currentPositionOverlay = this.getCurrentPositionMarker(latitude, longitude, this.state.currentPosition !== null);
    overlays = this.state.restaurants.map(marker => (
      <Overlay key={`overlay_${marker.identifier}`}
               anchor={[marker.latitude, marker.longitude]}
               payload={marker.identifier}>
        <img src='/images/pin.png'
             className="map_item__marker"
             data-payload={marker.identifier}
             onClick={this.onMarkerClicked.bind(this)}/>
      </Overlay>
    ));

    return (
      <Map center={[latitude, longitude]} zoom={12} width={this.props.width} height={height}>
        {overlays}
        {currentPositionOverlay}
      </Map>
    );
  }
}

MapItem.propTypes = {
  width: PropTypes.number.isRequired,
  onRestaurantClicked: PropTypes.func.isRequired
};

export default MapItem;