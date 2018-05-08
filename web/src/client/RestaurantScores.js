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
import MdStarOutline from 'react-icons/lib/md/star-outline';
import MdStar from 'react-icons/lib/md/star';
import MdStarHalf from 'react-icons/lib/md/star-half';
import {ListGroup, ListGroupItem} from 'react-bootstrap';
import uuid from 'react-native-uuid';
import PropTypes from 'prop-types';

class RestaurantScores extends Component {
  static createScoredLabel(score) {
    if (score === null) {
      return null;
    }
    const MAX_STARS = 5;
    score += 1;

    // Convert from semantic analysis score to 5-star score
    let stars = parseFloat(score) * MAX_STARS / 2;
    let hasRemainder = parseInt(stars) < stars;
    let html = [];

    // Adds filled stars
    for (let i = 0; i < parseInt(stars); i++) {
      html.push(<MdStar key={uuid.v4()}/>);
    }

    // Adds half star if score has remainder
    if (hasRemainder) {
      html.push(<MdStarHalf key={uuid.v4()}/>);
    }

    // Round to up the amount of stars for not adding too much stars
    stars += hasRemainder ? 1 : 0;
    for (let i = stars; i < MAX_STARS; i++) {
      html.push(<MdStarOutline key={uuid.v4()}/>);
    }
    return html;
  }

  render() {
    const
      serviceScore = RestaurantScores.createScoredLabel(this.props.serviceScore),
      priceScore = RestaurantScores.createScoredLabel(this.props.priceScore),
      foodScore = RestaurantScores.createScoredLabel(this.props.foodScore),
      locationScore = RestaurantScores.createScoredLabel(this.props.locationScore),
      totalScore = RestaurantScores.createScoredLabel(this.props.totalScore);
    return (
      <ListGroup>
        <ListGroupItem header="Food">{foodScore ? foodScore : 'N/A'}</ListGroupItem>
        <ListGroupItem header="Price">{priceScore ? priceScore : 'N/A'}</ListGroupItem>
        <ListGroupItem header="Service">{serviceScore ? serviceScore : 'N/A'}</ListGroupItem>
        <ListGroupItem header="Location">{locationScore ? locationScore : 'N/A'}</ListGroupItem>
        <ListGroupItem header="Average">{totalScore ? totalScore : 'N/A'}</ListGroupItem>
      </ListGroup>
    );
  }
}
PropTypes.propTypes = {
  foodScore: PropTypes.number,
  priceScore: PropTypes.number,
  serviceScore: PropTypes.number,
  locationScore: PropTypes.number,
  totalScore: PropTypes.number,
};

export default RestaurantScores;