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
import {Form, FormGroup, Col, FormControl, ControlLabel, Button} from 'react-bootstrap';

class ProjectForm extends Component {
  onFormSave() {
    const
      name = document.getElementById('name').value,
      description = document.getElementById('description').value;
    this.props.onSaveButtonClicked(name, description);
  }

  render() {
    return (
      <Form horizontal>
        <FormControl type="hidden" value={this.props.isEdit ? this.props.projectIdentifier : ''}/>
        <FormGroup controlId="name">
          <Col componentClass={ControlLabel} sm={2}>Project Name</Col>
          <Col sm={10}>
            <FormControl type="text" placeholder="The name of the project..."
                         name="name"
                         defaultValue={this.props.isEdit ? this.props.projectName : ''}/>
          </Col>
        </FormGroup>
        <FormGroup controlId="description">
          <Col componentClass={ControlLabel} sm={2}>Description</Col>
          <Col sm={10}>
            <FormControl componentClass="textarea" placeholder="Notes about the project..."
                         name="description"
                         defaultValue={this.props.isEdit ? this.props.projectDescription : ''}/>
          </Col>
        </FormGroup>
        <FormGroup controlId="newProject">
          <Col sm={12}>
            <Button onClick={this.onFormSave.bind(this)}>Save</Button>
          </Col>
        </FormGroup>
      </Form>
    );
  }
}

ProjectForm.propTypes = {
  isEdit: PropTypes.bool.isRequired,
  onSaveButtonClicked: PropTypes.func.isRequired,
  projectName: PropTypes.string,
  projectDescription: PropTypes.string,
  projectIdentifier: PropTypes.string,
};

export default ProjectForm;
