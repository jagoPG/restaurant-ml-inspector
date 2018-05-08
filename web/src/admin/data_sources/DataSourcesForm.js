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
import {Redirect} from 'react-router-dom';
import PropTypes from 'prop-types';
import {FormControl, FormGroup, ControlLabel, Button} from 'react-bootstrap';
import {
  requestGetCountries,
  requestGetRestaurantNetworkIdentifier,
  editDataSource,
  addDataSource
} from './../api';
import uuid from 'react-native-uuid';
import Loading from './../../common/LoadingModal/Loading';

class DataSourcesForm extends Component {
  constructor(props) {
    super(props);
    this.googlePlacesQuery = null;
    this.facebookQuery = null;

    this.state = {
      countries: [],
      google_restaurants: [],
      facebook_restaurants: [],
      isDownloadingData: false,
      redirectToHome: false,
    };

    this.fillGooglePlacesList = this.fillGooglePlacesList.bind(this);
    this.fillFacebookList = this.fillFacebookList.bind(this);
    this.fillCountryList = this.fillCountryList.bind(this);
    this.getGooglePlacesRestaurants = this.getGooglePlacesRestaurants.bind(this);
    this.getFacebookRestaurants = this.getFacebookRestaurants.bind(this);
  }

  componentDidMount() {
    requestGetCountries(this.fillCountryList);
  }

  componentWillReceiveProps(props) {
    this.setState({
      twitterName: props.twitterName ? props.twitterName : '',
      facebookName: props.facebookName ? props.facebookName : '',
      googlePlacesName: props.googlePlacesName ? props.googlePlacesName : '',
      selectedCountry: props.country,
    });
  }

  setDownloadingData(isLoading) {
    this.setState({isDownloadingData: isLoading});
  }

  onDownloadingDataError(error, code) {
    if (code === 400 && 'error' in error) {
      alert(error.error);
    }
    this.setDownloadingData(false);
  }

  fillCountryList(response) {
    this.setState({
      countries: response,
      selectedCountry: this.props.country
    });
  }

  getGooglePlacesRestaurants(event) {
    const name = event.target.value;
    this.setState({googlePlacesName: name});
    clearTimeout(this.googlePlacesQuery);

    if (event.target.value.length > 3) {
      this.googlePlacesQuery = setTimeout(
        this.requestSimilarPlacesAtSocialNetwork.bind(
          this, 'Google Places', name, this.fillGooglePlacesList
        ),
        1000
      );
    }
  }

  requestSimilarPlacesAtSocialNetwork(social_network, name, onSuccess) {
    const country = document.getElementById('country').value;

    requestGetRestaurantNetworkIdentifier(
      {country, name, network: social_network},
      onSuccess.bind(this),
      this.onDownloadingDataError.bind(this),
    );
    this.setDownloadingData(true);
  }

  getFacebookRestaurants(event) {
    const name = event.target.value;
    this.setState({facebookName: name});
    clearTimeout(this.facebookQuery);

    if (event.target.value.length > 3) {
      this.facebookQuery = setTimeout(
        this.requestSimilarPlacesAtSocialNetwork.bind(
          this, 'Facebook', name, this.fillFacebookList
        ),
        1000
      );
    }
  }

  fillGooglePlacesList(response) {
    this.setState({
      google_restaurants: response,
      isDownloadingData: false,
    });
  }

  fillFacebookList(response) {
    this.setState({
      facebook_restaurants: response,
      isDownloadingData: false,
    })
  }

  saveData() {
    const
      country = document.getElementById('country').value,
      twitterId = document.getElementById('twitter_name').value,
      facebookId = document.getElementById('facebook_id').value,
      googlePlaceId = document.getElementById('google_places_id').value,
      geoLocation = '40.463667,-3.74922';
    if (!twitterId && !googlePlaceId && !facebookId) {
      alert('New data has not been provided');
      return;
    }
    if (country === '') {
      alert('No country has been selected');
      return;
    }

    this.persistData(facebookId, 'Facebook', country, null, this.props.facebookName);
    this.persistData(twitterId, 'Twitter', null, geoLocation, this.props.twitterName);
    this.persistData(googlePlaceId, 'Google Places', country, null, this.props.googlePlacesName);

    this.setState({
      redirectToHome: true,
    });
  }

  persistData(restaurantId, socialNetwork, country = null, geoPosition = null, previousId = null) {
    if (previousId) {
      editDataSource({
        social_network: socialNetwork,
        restaurant_id: restaurantId,
        country: country,
        geo_position: geoPosition,
        project_id: this.props.projectId
      }, null);
    } else if (restaurantId) {
      addDataSource({
        social_network: socialNetwork,
        restaurant_id: restaurantId,
        country: country,
        geo_position: geoPosition,
        project_id: this.props.projectId
      }, null);
    }
  }

  componentWillUpdate(nextProps, nextState) {
    const country = document.getElementById('country');
    if (country) {
      nextState.selectedCountry = country.value;
    }
  }

  componentDidUpdate() {
    const country = document.getElementById('country');
    if (country) {
      country.value = this.state.selectedCountry;
    }
  }

  render() {
    const
      isFormReady = this.state.countries.length !== 0,
      loading = this.state.isDownloadingData ? <Loading/> : '';
    let form;
    if (this.state.redirectToHome) {
      return <Redirect to={`/admin/project/${this.props.projectId}/`}/>;
    }
    if (!isFormReady) {
      return <div>Loading form...</div>;
    }

    return (
      <form>
        <FormGroup controlId="country">
          <ControlLabel>Country</ControlLabel>
          <FormControl
            componentClass="select"
            placeholder="Your country...">
            {
              this.state.countries.map((country) => {
                return <option key={uuid.v4()}
                               value={country.code}>{country.name}</option>
              })
            }
          </FormControl>
        </FormGroup>
        <FormGroup controlId="google_places_name">
          <ControlLabel>Google Places</ControlLabel>
          <FormControl type="text"
                       placeholder="Your restaurant name"
                       value={this.state.googlePlacesName}
                       onChange={this.getGooglePlacesRestaurants}/>
        </FormGroup>
        <FormGroup controlId="google_places_id">
          <FormControl componentClass="select">
            {
              this.state.google_restaurants.map((item) => {
                return <option key={uuid.v4()}
                               value={item.id}>{item.name} ({item.address})</option>;
              })
            }
          </FormControl>
        </FormGroup>
        <FormGroup controlId="twitter_name">
          <ControlLabel>Twitter</ControlLabel>
          <FormControl type="text"
                       value={this.state.twitterName}
                       onChange={(evt) => {this.setState({twitterName: evt.target.value});}}
                       placeholder="#Artorias, @NukaCola, MyExample"/>
        </FormGroup>
        <FormGroup controlId="facebook_name">
          <ControlLabel>Facebook</ControlLabel>
          <FormControl type="text"
                       value={this.state.facebookName}
                       placeholder="Your facebook page name..."
                       onChange={this.getFacebookRestaurants}/>
        </FormGroup>
        <FormGroup controlId="facebook_id">
          <FormControl componentClass="select">
            {
              this.state.facebook_restaurants.map((item) => {
                return <option key={uuid.v4()}
                               value={item.id}>{item.name} ({item.address})</option>;
              })
            }
          </FormControl>
        </FormGroup>
        <Button onClick={this.saveData.bind(this)}>Save</Button>
        {loading}
      </form>
    );
  }
}

DataSourcesForm.propTypes = {
  country: PropTypes.string,
  facebookName: PropTypes.string,
  twitterName: PropTypes.string,
  googlePlacesName: PropTypes.string,
  projectId: PropTypes.string.isRequired,
};

export default DataSourcesForm;