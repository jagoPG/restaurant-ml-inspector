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
import PropTypes from 'prop-types';
import {Grid, Row, Col, Button, Breadcrumb} from 'react-bootstrap';
import GeneralProjectDetails from './GeneralProjectDetails';
import KeyPointTable from './KeyPointTable';
import {
  requestGetProject, requestGetProjectDetails, requestAnalysis, retrieveDataFromSocialNetworks
} from './../api';
import uuid from 'react-native-uuid';
import Loading from './../../common/LoadingModal/Loading';


class ProjectDetailsPage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      generalData: null,
      analysisData: null,
      isBusy: false,
      projectId: props.store.getState().projectId
    };
  }

  componentDidMount() {
    requestGetProject({projectId: this.state.projectId}, this.onProjectDataRetrieved.bind(this));
    this.setState({isBusy: true});
  }

  onProjectDataRetrieved(data) {
    if (data['analysis_id'] !== null) {
      this.setState({isBusy: true});
      requestGetProjectDetails({
          projectId: this.state.projectId
        },
        this.onProjectDetailsRetrieved.bind(this)
      );
    }
    this.dispatchChangeOfTitle(data.name);

    this.setState({
      generalData: data,
      isBusy: false
    });
  }

  dispatchChangeOfTitle(name) {
    this.props.store.dispatch({
      type: 'SET_TITLE',
      projectId: this.state.projectId,
      title: name
    });
  }

  onProjectDetailsRetrieved(data) {
    this.setState({
      analysisData: data,
      isBusy: false,
    });
  }

  analyse() {
    this.requestRetrieveDataFromSources();
    this.setState({isBusy: true});
  }

  requestRetrieveDataFromSources() {
    retrieveDataFromSocialNetworks(
      {projectId: this.state.projectId},
      this.onRequestRetrieveDataSuccess.bind(this),
      this.onRequestRetrieveDataFailed.bind(this)
    );
  }

  onRequestRetrieveDataSuccess() {
    this.requestProjectAnalysis()
  }

  onRequestRetrieveDataFailed() {
    alert(
      'There has been any problem during the analysis. Try again later or notify to' +
      ' the site administrator if the problem persists.'
    );
    this.setState({
      isBusy: false
    });
  }

  requestProjectAnalysis() {
    requestAnalysis(
      {projectId: this.state.projectId},
      this.onRequestProjectAnalysisSuccess.bind(this),
      this.onRequestProjectAnalysisFailed.bind(this)
    );
  }

  onRequestProjectAnalysisSuccess() {
    requestGetProject(
      {projectId: this.state.projectId}, this.onProjectDataRetrieved.bind(this)
    );
  }

  onRequestProjectAnalysisFailed() {
    alert(
      'There has been any problem during the analysis. Try again later or notify to' +
      ' the site administrator if the problem persists.'
    );
    this.setState({
      isBusy: false
    });
  }

  render() {
    if (this.state.redirectHome) {
      return <Redirect to="/admin/"/>
    }
    let loadingModal;
    const dataSourcesLink = `/admin/project/${this.state.projectId}/data-sources/`;

    if (this.state.isBusy) {
      if (this.state.isBusy) {
        loadingModal = <Loading/>;
      }
      return this.renderNoDataPage(
        <Row className="show-grid">
          <h2>Loading data...</h2>
          {loadingModal}
        </Row>
      );
    } else if (this.state.analysisData === null) {
      return this.renderNoDataPage(
        <Row className="show-grid">
          <h2>No analysis has been executed yet</h2>
        </Row>
      );
    }


    return (
      <div>
        <Grid>
          <Row className="show-grid">
            <Col sm={12}>
              <Breadcrumb>
                <Breadcrumb.Item onClick={() => {this.setState({redirectHome: true})}}>Projects</Breadcrumb.Item>
                <Breadcrumb.Item active>{this.state.generalData.name}</Breadcrumb.Item>
              </Breadcrumb>
            </Col>
          </Row>
          <Row className="show-grid">
            <Col sm={10}>
              <Link
                className="btn btn-default"
                to={dataSourcesLink}
                onClick={() => {
                  this.props.store.dispatch({
                    type: 'VIEW_PROJECT',
                    projectId: this.state.projectId,
                    projectName: this.state.generalData ? this.state.generalData.name : null
                  })
                }}
                disabled={this.state.isBusy}>Set up Sources</Link>
            </Col>
            <Col sm={2}>
              <Button
                onClick={this.analyse.bind(this)}
                disabled={this.state.isBusy}>Analyse</Button>
            </Col>
          </Row>
          <Row className="show-grid">
            <Col sm={12}>
              <h2>General Information</h2>
              <GeneralProjectDetails restaurant_data={this.state.analysisData.restaurant_data}/>
            </Col>
          </Row>
          <Row className="show-grid">
            <Col sm={6}>
              <h2>Strong Points</h2>
              <KeyPointTable
                projectId={this.state.projectId}
                key={uuid.v4()}
                elements={this.state.analysisData.good_key_points}/>
            </Col>
            <Col sm={6}>
              <h2>Improvement Areas</h2>
              <KeyPointTable
                projectId={this.state.projectId}
                key={uuid.v4()}
                elements={this.state.analysisData.improvement_key_points}/>
            </Col>
          </Row>
        </Grid>
      </div>
    );
  }

  renderNoDataPage(resultData) {
    const dataSourcesLink = `/admin/project/${this.state.projectId}/data-sources/`;
    return (
      <Grid>
        <Row className="show-grid">
          <Col sm={12}>
            <Breadcrumb>
              <Breadcrumb.Item href="/admin/">Projects</Breadcrumb.Item>
              <Breadcrumb.Item active>Details</Breadcrumb.Item>
            </Breadcrumb>
          </Col>
        </Row>
        <Row className="show-grid">
          <Col sm={10}>
            <Link
              className="btn btn-default"
              to={dataSourcesLink}
              disabled={this.state.isBusy}>Set up Sources</Link>
          </Col>
          <Col sm={2}>
            <Button
              onClick={this.analyse.bind(this)}
              disabled={this.state.isBusy}>Analyse</Button>
          </Col>
        </Row>
        {resultData}
      </Grid>
    );
  }
}

ProjectDetailsPage.propTypes = {
  store: PropTypes.object.isRequired,
};

export default ProjectDetailsPage;