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
import {Modal, Button} from 'react-bootstrap';
import {requestRestaurantDefaults} from './api';
import PropTypes from 'prop-types';
import RestaurantInformation from './RestaurantInformation';
import RestaurantScores from './RestaurantScores';

const
  MODAL_SCORES = 1,
  MODAL_INFORMATION = 2;

class RestaurantModal extends Component {
  constructor(props) {
    super(props);

    this.state = {
      information: null,
      modal: MODAL_SCORES
    };
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.props.projectId !== prevProps.projectId) {
      this.retrieveProjectInformation();
    }
  }

  retrieveProjectInformation() {
    const projectId = this.props.projectId;
    if (!projectId) {
      return;
    }
    requestRestaurantDefaults({projectId}, this.onProjectInformationRetrieved.bind(this));
  }

  onProjectInformationRetrieved(response) {
    this.setState({
      information: response,
    });
  }

  switchModal() {
    let nextState;
    nextState = this.state.modal === MODAL_SCORES ? MODAL_INFORMATION : MODAL_SCORES;
    console.log(this.state.modal);
    this.setState({
      modal: nextState
    });
  }

  static renderRestaurantInformation(information) {
    const
      description = information.description,
      address = information.address,
      telephone = information.telephone,
      openingHours = information.opening_hours;

    return (
      <RestaurantInformation
        description={description}
        address={address}
        telephone={telephone}
        openingHours={openingHours}/>
    );
  }

  static renderRestaurantScores(information) {
    const scores = information.scores;
    return (
      <RestaurantScores
        foodScore={scores.food}
        priceScore={scores.price}
        serviceScore={scores.service}
        locationScore={scores.location}
        totalScore={scores.total}/>
    );
  }

  render() {
    if (this.props.projectId === null || this.state.information === null) {
      return '';
    }
    let body;
    if (this.state.modal === MODAL_SCORES) {
      body = RestaurantModal.renderRestaurantScores(this.state.information);
    } else {
      body = RestaurantModal.renderRestaurantInformation(this.state.information);
    }
    const title = this.state.information.name;

    return (
      <div className="static-modal">
        <Modal.Dialog>
          <Modal.Header>
            <Modal.Title>{title}</Modal.Title>
          </Modal.Header>

          <Modal.Body>
            {body}
          </Modal.Body>

          <Modal.Footer>
            <Button onClick={this.props.clearRestaurantClicked.bind(this)}>Close</Button>
            <Button onClick={this.switchModal.bind(this)} bsStyle="primary">{this.state.modal === MODAL_SCORES ? 'Details' : 'Scores'}</Button>
          </Modal.Footer>
        </Modal.Dialog>
      </div>
    );
  }
}

PropTypes.propTypes = {
  projectId: PropTypes.string,
  clearRestaurantClicked: PropTypes.func.isRequired
};

export default RestaurantModal;