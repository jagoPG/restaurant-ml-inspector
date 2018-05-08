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
import {Link, Redirect} from 'react-router-dom';
import ProjectForm from './ProjectForm';
import PropTypes from 'prop-types';
import {Breadcrumb} from 'react-bootstrap';
import {editProject, requestGetProject} from './../api';

class EditProjectPage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      project: null,
      redirectHome: false,
      redirectToProject: false,
      projectId: props.store.getState().projectId
    };
    this.onSaveButtonClicked = this.onSaveButtonClicked.bind(this);
  }

  componentDidMount() {
    this.props.store.dispatch({
      type: 'SET_TITLE',
      projectId: this.state.projectId,
      title: 'Edit project'
    });
    requestGetProject({
      projectId: this.state.projectId
    }, this.loadProjectData.bind(this));
  }

  loadProjectData(response) {
    this.setState({
      project: response
    });
  }

  onSaveButtonClicked(name, description) {
    const projectId = this.state.projectId;
    editProject({projectId, name, description}, null);
    this.setState({redirectToProject: true});
  }

  render() {
    const project = this.state.project;
    if (this.state.redirectHome) {
      return <Redirect to="/admin/"/>;
    }
    if (this.state.redirectToProject) {
      const projectLink = `/admin/project/${this.state.projectId}/`;
      return <Redirect to={projectLink}/>;
    }
    if (project === null) {
      return  <div>Loading...</div>;
    }

    return (
      <div>
        <Breadcrumb>
          <Breadcrumb.Item onClick={() => {this.setState({redirectHome: true})}}>Projects</Breadcrumb.Item>
          <Breadcrumb.Item onClick={() => {
            this.setState({redirectToProject: true})
          }}>{this.state.project.name}</Breadcrumb.Item>
          <Breadcrumb.Item active>Edit Project</Breadcrumb.Item>
        </Breadcrumb>
        <h4>Modify your amazing project.</h4>
        <ProjectForm
          isEdit={true}
          onSaveButtonClicked={this.onSaveButtonClicked}
          projectIdentifier={project.identifier}
          projectName={project.name}
          projectDescription={project.description}/>
      </div>
    );
  }
}

EditProjectPage.propTypes = {
  store: PropTypes.object.isRequired
};

export default EditProjectPage;