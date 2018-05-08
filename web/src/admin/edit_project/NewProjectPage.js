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
import {Breadcrumb} from 'react-bootstrap';
import {createProject} from './../api';

class NewProjectPage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      redirectHome: false,
    };
  }

  componentDidMount() {
    this.props.store.dispatch({
      type: 'SET_TITLE',
      projectId: null,
      title: 'New project'
    });
  }

  onSaveButtonClicked(name, description) {
    createProject({name, description}, null);
    this.setState({
      redirectHome: true,
    });
  }

  render() {
    if (this.state.redirectHome) {
      return <Redirect to="/admin/"/>;
    }

    return (
      <div>
        <Breadcrumb>
          <Breadcrumb.Item onClick={() => {this.setState({redirectHome: true})}}>Projects</Breadcrumb.Item>
          <Breadcrumb.Item active>New Project</Breadcrumb.Item>
        </Breadcrumb>
        <h4>
          Create a new amazing project and download its social network content in order to get information about
          your clients.
        </h4>
        <ProjectForm isEdit={false} onSaveButtonClicked={this.onSaveButtonClicked.bind(this)}/>
      </div>
    );
  }
}

export default NewProjectPage;