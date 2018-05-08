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
import ProjectListFormItem from './ProjectListFormItem';
import {confirmAlert} from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import PropTypes from 'prop-types';
import {Table} from 'react-bootstrap';

class ProjectListForm extends Component {
  constructor(props) {
    super(props);

    this.onDeleteButtonClickedFnc = this.onDeleteButtonClicked.bind(this);
  }

  onDeleteButtonClicked(projectIdentifier, projectName) {
    confirmAlert({
      title: 'Confirmation',
      message: `Are you sure you want to delete ${projectName} project?`,
      confirmLabel: 'Yes',
      cancelLabel: 'No',
      onConfirm: this.removeProject.bind(this, projectIdentifier),
    });
  }

  removeProject(projectIdentifier) {
    this.props.removeProject(projectIdentifier);
  }

  render() {
    return (
      <Table>
        <thead>
        <tr>
          <th>Project</th>
          <th>Created On</th>
          <th>Actions</th>
        </tr>
        </thead>
        <tbody>
        {
          this.props.projects.map((element) => {
            return <ProjectListFormItem key={element.identifier}
                                        projectName={element.name}
                                        projectCreatedOn={element.created_on}
                                        projectIdentifier={element.identifier}
                                        onDeleteButtonClicked={this.onDeleteButtonClickedFnc}
                                        store={this.props.store}/>
          })
        }
        </tbody>
      </Table>
    );
  }
}

ProjectListForm.propTypes = {
  removeProject: PropTypes.func.isRequired,
  projects: PropTypes.array,
  store: PropTypes.object.isRequired,
};

export default ProjectListForm;