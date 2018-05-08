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
import {Button} from 'react-bootstrap';
import './AuthenticationWindow.scss';

class AuthenticationWindow extends Component {
  renderAuthentication() {
    return (
      <div className="authentication">
        <h1>Greetings visitor!</h1>
        <div className="authentication-wrapper">
          <div className="authentication-info">
            <div className="authentication-info__body">
              <h4>
                Access to your projects and keep your business growing with us.
              </h4>
            </div>
            <div className="authentication-info__bottom">
              <Button onClick={() => location.href = '/auth/login'}>Log in</Button>
            </div>
          </div>
          <div className="authentication-info">
            <div className="authentication-info__body">
              <h4>
                Do you have not any account? Use your Google account for requesting access to the
                platform. Soon an administrator will contact with you for granting access to the
                back-office.
              </h4>
            </div>
            <div className="authentication-info__bottom">
              <Button onClick={() => location.href = '/auth/register'}>Register</Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  renderSuccessRegistered() {
    return (
      <div className="authentication">
        <h1>Greetings visitor!</h1>
        <div className="authentication-wrapper">
          <div className="authentication-info">
            <div className="authentication-info__body">
              <h4>
                You have successfully registered. Soon a site administrator will contact with you for
                activating your account. Thank you for your patience.
              </h4>
            </div>
          </div>
        </div>
      </div>
    );
  }

  renderError(errorMessage) {
    return (
      <div className="authentication">
        <h1>Something wrong happened!</h1>
        <div className="authentication-wrapper">
          <div className="authentication-info">
            <div className="authentication-info__body">
              <h4>
                {errorMessage.text.trim()}
              </h4>
            </div>
          </div>
        </div>
      </div>
    );
  }

  render() {
    const
      path = location.pathname,
      errorMessage = document.getElementById('error');
    if (path === '/auth/') {
      return this.renderAuthentication();
    } else if (path === '/auth/register/registered/') {
      if (errorMessage === null) {
        return this.renderSuccessRegistered();
      }
    }
    return this.renderError(errorMessage);
  }
}

export default AuthenticationWindow;