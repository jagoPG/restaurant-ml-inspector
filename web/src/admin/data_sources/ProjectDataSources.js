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
import {Redirect} from 'react-router-dom';
import PropTypes from 'prop-types';
import {Grid, Breadcrumb, Row, Col} from 'react-bootstrap';
import DataSourcesForm from './DataSourcesForm';
import {requestGetProjectDataSources} from './../api';

class ProjectDataSources extends Component {
  constructor(props) {
    super(props);

    this.state = {
      projectId: props.store.getState().projectId,
      projectName: props.store.getState().projectName,
      googlePlacesName: null,
      facebookName: null,
      twitterName: null,
      country: null
    };
  }

  componentDidMount() {
    requestGetProjectDataSources({
      projectId: this.state.projectId
    }, this.onSourcesRetrieved.bind(this));
    this.props.store.dispatch({
      type: 'SET_TITLE',
      projectId: this.state.projectId,
      title: this.state.projectId
    });
  }

  onSourcesRetrieved(response) {
    let twitterName = null, googlePlacesName = null, facebookName = null, country = null;
    response.map((item) => {
      if (item.country) {
        country = item.country;
      }
      switch (item.social_network_name) {
        case 'Twitter':
          twitterName = item.restaurant_name;
          break;
        case 'Google Places':
          googlePlacesName = item.restaurant_name;
          break;
        case 'Facebook':
          facebookName = item.restaurant_name;
          break;
      }
    });
    this.setState({
      facebookName: facebookName,
      twitterName: twitterName,
      googlePlacesName: googlePlacesName,
      country: country
    });
  }

  render() {
    if (this.state.redirectToProject) {
      const projectLink = `/admin/project/${this.state.projectId}/`;
      return <Redirect to={projectLink}/>;
    }
    if (this.state.redirectToHome) {
      return <Redirect to="/admin/"/>;
    }
    return (
      <div>
        <Grid>
          <Row className="show-grid">
            <Col sm={12}>
              <Breadcrumb>
                <Breadcrumb.Item onClick={() => this.setState({redirectToHome: true})}>Projects</Breadcrumb.Item>
                <Breadcrumb.Item onClick={() => this.setState({redirectToProject: true})}>{this.state.projectName ? this.state.projectName : this.state.projectId}</Breadcrumb.Item>
                <Breadcrumb.Item active>Data Sources</Breadcrumb.Item>
              </Breadcrumb>
            </Col>
            <Col sm={12}>
              <DataSourcesForm
                projectId={this.state.projectId}
                facebookName={this.state.facebookName}
                googlePlacesName={this.state.googlePlacesName}
                twitterName={this.state.twitterName}
                country={this.state.country}/>
            </Col>
          </Row>
        </Grid>
      </div>
    );
  }
}

ProjectDataSources.propTypes = {
  store: PropTypes.object.isRequired
};

export default ProjectDataSources;