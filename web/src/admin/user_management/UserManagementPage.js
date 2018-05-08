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
import {confirmAlert} from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import {Redirect} from 'react-router-dom';
import {Breadcrumb, Table} from 'react-bootstrap';
import {requestUsers, updateUserRoles, activateUser, deactivateUser} from './../api';
import UserTableItem from './UserTableItem';

class UserManagementPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      users: null,
      redirectHome: false
    };
    requestUsers(this.onUserRequestedSuccess.bind(this));
  }

  onUserRequestedSuccess(data) {
    this.setState({
      users: data
    });
  }

  onRoleUpdateClicked(identifier, roles) {
    updateUserRoles({userIdentifier: identifier, roles}, () => {
      window.alert('User permissions have been updated');
    }, null);
  }

  onDeactivate(userIdentifier, userName) {
    confirmAlert({
      title: 'Confirmation',
      message: 'Are you sure you want to revoke ' + userName + ' user?',
      confirmLabel: 'Yes',
      cancelLabel: 'No',
      onConfirm: () => {
        deactivateUser(userIdentifier, () => {
          this.switchUserStatus(userIdentifier, false);
        });
      },
    });
  }

  onActivateButtonClicked(userIdentifier) {
    activateUser(userIdentifier, () => {
      this.switchUserStatus(userIdentifier, true);
    });
  }

  switchUserStatus(userIdentifier, isVerified) {
    for (let index = 0; index < this.state.users.length; index++) {
      let user = this.state.users[index];
      if (user.identifier === userIdentifier) {
        user.is_verified = isVerified;
        break;
      }
    }
    this.setState({
      users: this.state.users
    });
  }

  render() {
    if (this.state.redirectHome) {
      return <Redirect to="/admin/"/>;
    }
    if (this.state.users === null) {
      return <h3>Loading users...</h3>
    } else if (this.state.users.length === 0) {
      return <h3>There are no registered users.</h3>
    }
    return (
      <div>
        <Breadcrumb>
          <Breadcrumb.Item href="#" onClick={() => this.setState({redirectHome: true}) }>Projects</Breadcrumb.Item>
          <Breadcrumb.Item active>User Management</Breadcrumb.Item>
        </Breadcrumb>
        <Table>
          <thead>
          <tr>
            <th>User</th>
            <th>Last Access</th>
            <th>Roles</th>
            <th>Actions</th>
          </tr>
          </thead>
          <tbody>
          {
            this.state.users.map((element) => {
              return <UserTableItem key={element.identifier}
                                    name={element.name + ' ' + element.surnames}
                                    lastAccess={element.last_access}
                                    identifier={element.identifier}
                                    isVerified={element.is_verified}
                                    roles={element.roles}
                                    onDeactivateButtonClicked={this.onDeactivate.bind(this)}
                                    onActivateButtonClicked={this.onActivateButtonClicked.bind(this)}
                                    onUpdateRoleButtonClicked={this.onRoleUpdateClicked.bind(this)}/>
            })
          }
          </tbody>
        </Table>
      </div>
    );
  }
}

export default UserManagementPage;