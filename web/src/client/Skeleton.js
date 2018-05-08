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
import {Navbar, Nav, NavItem} from 'react-bootstrap';
import MapArea from './MapArea';
import BetaBanner from './../common/BetaBanner/BetaBanner';

class Skeleton extends Component {
  constructor(props) {
    super(props);

    this.state = {
      title: 'Restaurant Locator',
    }
  }

  render() {
    return (
      <div>
        <Navbar inverse collapseOnSelect>
          <Navbar.Header>
            <Navbar.Brand>
              <a href="/">{this.state.title}</a>
            </Navbar.Brand>
            <Navbar.Toggle/>
          </Navbar.Header>
          <Navbar.Collapse>
            <Nav pullRight>
              <NavItem
                eventKey={1}
                onClick={() => window.open('/file/RestaurantWebAppDoc.pdf', '_blank')}
              >Show me the doc!</NavItem>
              <NavItem
                eventKey={2}
                onClick={() => location.href = '/admin/'}
              >Back-Office</NavItem>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
        <MapArea/>
        <BetaBanner/>
      </div>
    );
  }
}

export default Skeleton;