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
import './GeneralProjectDetails.scss';

class GeneralProjectDetails extends Component {
  render() {
    return (
      <ListGroup>
        <ListGroupItem>
          <MdLocation size={28}/>
          <span className="general_project__data">{this.props.restaurant_data.address}</span>
        </ListGroupItem>
        <ListGroupItem>
          <MdPhone size={28}/>
          <span className="general_project__data">{this.props.restaurant_data.telephone}</span>
        </ListGroupItem>
        <ListGroupItem>
          <MdDescription size={28}/>
          <span className="general_project__data">{this.props.restaurant_data.description}</span>
        </ListGroupItem>
        <ListGroupItem>
          <p><MdSchedule size={28}/></p>
          <p className="general_project__paragraph" dangerouslySetInnerHTML={{
            __html: this.props.restaurant_data.opening_hours
          }}></p>
        </ListGroupItem>
      </ListGroup>
    );
  }
}

GeneralProjectDetails.propTypes = {
  restaurant_data: PropTypes.object.isRequired
};

export default GeneralProjectDetails;