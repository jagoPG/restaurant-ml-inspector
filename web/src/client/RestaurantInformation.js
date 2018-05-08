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
import PropTypes from 'prop-types';
import {ListGroup, ListGroupItem} from 'react-bootstrap';
import MdDescription from 'react-icons/lib/md/description';
import MdLocation from 'react-icons/lib/md/location-city';
import MdPhone from 'react-icons/lib/md/phone';
import MdSchedule from 'react-icons/lib/md/schedule';
import './RestaurantInformation.scss';

class RestaurantInformation extends Component {
  render() {
    return (
      <ListGroup>
        <ListGroupItem>
          <div>
            <p><MdDescription size={28}/></p>
            <p
              className="restaurant_information__paragraph">{this.props.description ? this.props.description : 'N/A'}</p>
          </div>
        </ListGroupItem>
        <ListGroupItem>
          <div>
            <MdLocation size={28}/><span
            className="restaurant_information__data">{this.props.address ? this.props.address : 'N/A'}</span>
          </div>
        </ListGroupItem>
        <ListGroupItem>
          <div>
            <MdPhone size={28}/><span
            className="restaurant_information__data">{this.props.telephone ? this.props.telephone : 'N/A'}</span>
          </div>
        </ListGroupItem>
        <ListGroupItem>
          <div>
            <p><MdSchedule size={28}/></p>
            {this.props.openingHours ? <p className="restaurant_information__paragraph"
                                          dangerouslySetInnerHTML={{__html: this.props.openingHours}}></p> : 'N/A'}
          </div>
        </ListGroupItem>
      </ListGroup>
    );
  }
}

PropTypes.propTypes = {
  description: PropTypes.string.isRequired,
  address: PropTypes.string.isRequired,
  telephone: PropTypes.string.isRequired,
  openingHours: PropTypes.string.isRequired,
};

export default RestaurantInformation;