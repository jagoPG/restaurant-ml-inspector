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
import {Link} from 'react-router-dom';
import {Row, Col} from 'react-bootstrap';
import ProjectListForm from './ProjectListForm';
import {requestGetProjects, deleteProject} from './../api';
import PropTypes from 'prop-types';

class ProjectsListPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      projects: [],
    };
    requestGetProjects(this.onProjectDataRetrieved.bind(this));
  }

  componentDidMount() {
    this.props.store.dispatch({
      type: 'SET_TITLE',
      projectId: null,
      title: 'List of projects'
    });
  }

  onProjectDataRetrieved(data) {
    this.setState({
      projects: data
    })
  }

  removeProject(projectIdentifier) {
    deleteProject(
      {projectId: projectIdentifier},
      this.removeProjectFromList.bind(this, projectIdentifier)
    );
  }

  removeProjectFromList(projectIdentifier) {
    let
      projects = this.state.projects,
      index = 0;
    for (index; index < projects.length; index++) {
      if (projectIdentifier === projects[index].identifier) {
        break;
      }
    }
    projects.splice(index, 1);
    this.setState({
      projects: projects
    });
  }

  render() {
    let userManagement = null
    if (this.props.isAdmin) {
      userManagement = (
        <Link to="/admin/users/" className="btn btn-default">Users</Link>
      );
    }
    return (
      <div>
        <Row className="show-grid">
          <Col xs={9} sm={10}>
            <Link to="/admin/projects/new/" className="btn btn-primary">New Project</Link>
          </Col>
          <Col xs={1} sm={1}>
            {userManagement}
          </Col>
        </Row>
        <Row>
          <Col sm={12}>
            <ProjectListForm
              projects={this.state.projects}
              removeProject={this.removeProject.bind(this)}
              store={this.props.store}/>
          </Col>
        </Row>
      </div>
    );
  }
}

ProjectsListPage.propTypes = {
  store: PropTypes.object.isRequired,
};

export default ProjectsListPage;