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
import {Modal, ListGroup} from 'react-bootstrap';
import uuid from 'react-native-uuid';
import ReviewModalItem from './ReviewModalItem';

class ReviewModal extends Component {
  render() {
    return (
      <Modal
        show={this.props.isActive}
        onHide={this.props.onClose}
        bsSize="large"
        aria-labelledby="contained-modal-title-lg">
        <Modal.Header closeButton>
          <Modal.Title>Reviews containing {this.props.keyword}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <ListGroup>
            {
              this.props.reviews.map((review) => {
                return (
                  <ReviewModalItem
                    key={uuid.v4()}
                    text={review.text}
                    reviewId={review.reference}
                    projectId={this.props.projectId}
                    karma={review.karma}/>
                )
              })
            }
          </ListGroup>
        </Modal.Body>
      </Modal>
    );
  }
}

ReviewModal.propTypes = {
  projectId: PropTypes.string.isRequired,
  keyword: PropTypes.string,
  reviews: PropTypes.array,
  onClose: PropTypes.func.isRequired,
  isActive: PropTypes.bool.isRequired
};

export default ReviewModal;