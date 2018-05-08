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
import {Label} from 'react-bootstrap';
import './KeyPointItem.scss';

class KeyPointItem extends Component {
  showModal() {
    this.props.showModal(this.props.name, this.props.reviews);
  }

  render() {
    const karma = this.props.karma;
    let label, message;
    if (karma > .3) {
      label = 'success';
      message = 'Good';
    } else if (karma <= .3 && karma >= 0) {
      label = 'warning';
      message = 'Fair';
    } else if (karma < 0 && karma >= -.4) {
      label = 'danger';
      message = 'Bad';
    } else {
      label = 'danger';
      message = 'Very bad';
    }

    return (
      <tr>
        <td><span className="key-point-item" onClick={this.showModal.bind(this)}>{this.props.name}</span></td>
        <td>{this.props.appearances}</td>
        <td><Label bsStyle={label}>{message}</Label></td>
      </tr>
    );
  }
}

KeyPointItem.propTypes = {
  name: PropTypes.string.isRequired,
  appearances: PropTypes.number.isRequired,
  karma: PropTypes.number.isRequired,
  reviews: PropTypes.array.isRequired,
  showModal: PropTypes.func.isRequired
};

export default KeyPointItem;