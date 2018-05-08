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
import {BrowserRouter, Route, Link} from 'react-router-dom';
import ProjectsListPage from './project_list/ProjectsListPage';
import NewProjectPage from './edit_project/NewProjectPage';
import EditProjectPage from './edit_project/EditProjectPage';
import ProjectDetailsPage from './project_details/ProjectDetailsPage';
import UserManagementPage from './user_management/UserManagementPage';
import {Navbar, Nav, NavItem, Grid} from 'react-bootstrap';
import ProjectDataSources from './data_sources/ProjectDataSources';
import BetaBanner from './../common/BetaBanner/BetaBanner';
import {createStore} from 'redux';
import {renderPage} from './reducers/RenderPageStore';

const store = createStore(renderPage);

class Skeleton extends Component {
  constructor(props) {
    super(props);

    this.state = {
      roles: document.getElementById('user_roles').value,
    };
    store.subscribe(this.changeTitle.bind(this));
  }

  changeTitle() {
    if (!store.getState().title) {
      return;
    }
    this.setState({
      title: store.getState().title
    });
  }

  render() {
    return (
      <div>
        <Navbar inverse collapseOnSelect>
          <Navbar.Header>
            <Navbar.Brand>
              <a href="/admin/">{
                this.state.title ? this.state.title : 'List of projects'}
              </a>
            </Navbar.Brand>
            <Navbar.Toggle/>
          </Navbar.Header>

          <Navbar.Collapse>
            <Nav pullRight>
              <NavItem
                eventKey={1}
                onClick={() => {
                  window.open('https://dev.welive.eu/ideas_explorer/-/ideas_explorer_contest/28201/view', '_blank')
                }}>About</NavItem>
              <NavItem
                eventKey={1}
                onClick={() => window.open('/file/RestaurantWebAppDoc.pdf', '_blank')}
              >Show me the docs!</NavItem>
              <NavItem
                eventKey={1}
                onClick={() => location.href = '/auth/logout/'}
              >Log out</NavItem>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
        <BrowserRouter>
          <Grid>
            <Route exact path="/admin/"
                   render={() => <ProjectsListPage store={store} isAdmin={this.state.roles.indexOf('ADMIN') !== -1}/>}/>
            <Route exact path="/admin/projects/new/"
                   render={() => <NewProjectPage store={store}/>}/>
            <Route exact path="/admin/project/edit/:id/"
                   render={() => <EditProjectPage store={store}/>}/>
            <Route exact path="/admin/project/:id/"
                   render={() => <ProjectDetailsPage store={store}/>}/>
            <Route exact path={"/admin/project/:id/data-sources/"}
                   render={() => <ProjectDataSources store={store}/>}/>
            <Route exact path={"/admin/users/"}
                   render={() => <UserManagementPage store={store}/>}/>
          </Grid>
        </BrowserRouter>
        <BetaBanner/>
      </div>
    );
  }
}

export default Skeleton;