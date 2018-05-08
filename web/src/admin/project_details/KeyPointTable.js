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
import {Table} from 'react-bootstrap';
import KeyPointItem from './KeyPointItem';
import ReviewModal from './ReviewModal';
import uuid from 'react-native-uuid';

class KeyPointTable extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isModalActive: false,
      modalKeyword: null,
      modalReviews: []
    }
  }

  hideModal() {
    this.setState({
      isModalActive: false,
    });
  }

  showModal(keyword, reviews) {
    this.setState({
      isModalActive: true,
      modalKeyword: keyword,
      modalReviews: reviews
    })
  }

  render() {
    return (
      <div>
        <Table>
          <thead>
          <tr>
            <th>Keyword</th>
            <th>Appearances</th>
            <th>Karma</th>
          </tr>
          </thead>
          <tbody>
          {
            this.props.elements.map((element) => {
              return <KeyPointItem key={uuid.v4()}
                                   projectId={this.props.projectId}
                                   name={element.name}
                                   karma={element.karma}
                                   appearances={element.appearances}
                                   reviews={element.reviews}
                                   showModal={this.showModal.bind(this)}/>
            })
          }
          </tbody>
        </Table>
        <ReviewModal isActive={this.state.isModalActive}
                     projectId={this.props.projectId}
                     onClose={this.hideModal.bind(this)}
                     keyword={this.state.modalKeyword}
                     reviews={this.state.modalReviews}/>
      </div>
    );
  }
}

KeyPointTable.propTypes = {
  projectId: PropTypes.string.isRequired,
  elements: PropTypes.array.isRequired
};

export default KeyPointTable;