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
import ReactDOM from 'react-dom'
import PropTypes from 'prop-types';
import MdCheck from 'react-icons/lib/md/check';
import MdClose from 'react-icons/lib/md/close';
import MdSave from 'react-icons/lib/md/save';
import {FormControl} from 'react-bootstrap';

class UserTableItem extends Component {
  onRevokeClicked() {
    this.props.onDeactivateButtonClicked(this.props.identifier);
  }

  onActivateClicked() {
    this.props.onActivateButtonClicked(this.props.identifier, this.props.name);
  }

  onSaveClicked() {
    const options = ReactDOM.findDOMNode(this.roles).options;
    let roles = [];
    for (let index = 0; index < options.length; index++) {
      let option = options[index];
      if (option.selected) {
        roles.push(option.value);
      }
    }
    this.props.onUpdateRoleButtonClicked(this.props.identifier, roles);
  }

  render() {
    const action = this.props.isVerified ?
      <MdClose onClick={this.onRevokeClicked.bind(this)} size={28}/> :
      <MdCheck onClick={this.onActivateClicked.bind(this)} size={28}/>;
    return (
      <tr>
        <td>{this.props.name}</td>
        <td>{this.props.lastAccess ? this.props.lastAccess : 'Never'}</td>
        <td>
          <FormControl componentClass="select"
                       multiple
                       defaultValue={this.props.roles}
                       ref={(input) => { this.roles = input; }}>
            <option value="ADMIN">Administrator</option>
            <option value="DEVELOPER">Developer</option>
            <option value="BUSINESSMAN">Businessman</option>
          </FormControl>
        </td>
        <td>{action} <MdSave onClick={this.onSaveClicked.bind(this)} size={28}/></td>
      </tr>
    );
  }
}

UserTableItem.propTypes = {
  name: PropTypes.string.isRequired,
  lastAccess: PropTypes.string,
  identifier: PropTypes.string.isRequired,
  roles: PropTypes.array.isRequired,
  isVerified: PropTypes.bool.isRequired,
  onDeactivateButtonClicked: PropTypes.func.isRequired,
  onActivateButtonClicked: PropTypes.func.isRequired,
  onUpdateRoleButtonClicked: PropTypes.func.isRequired
};

export default UserTableItem;