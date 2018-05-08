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
import MdDone from 'react-icons/lib/md/done';
import MdClear from 'react-icons/lib/md/clear';
import {editReviewSentiment, markReviewAsSpam} from './../api.js';
import {ListGroupItem, Label} from 'react-bootstrap';
import './ReviewModalItem.scss';

class ReviewModalItem extends Component {
  markPositiveSentiment() {
    editReviewSentiment({
      project_id: this.props.projectId,
      review_id: this.props.reviewId,
      sentiment: 1
    }, () => {
      alert('The review has marked as positive review. Changes will be applied in the next analysis.')
    });
  }

  markNegativeSentiment() {
    editReviewSentiment({
      project_id: this.props.projectId,
      review_id: this.props.reviewId,
      sentiment: -1
    }, () => {
      alert('The review has marked as negative review. Changes will be applied in the next analysis.')
    });
  }

  markAsSpam() {
    markReviewAsSpam({
      project_id: this.props.projectId,
      review_id: this.props.reviewId,
      is_spam: true
    }, () => {
      alert('The review has marked as spam. Changes will be applied in the next analysis.')
    });
  }

  getSentimentMarker(karma) {
    let label, message;
    if (karma > .3) {
      label = 'success';
      message = 'Good';
    } else if (karma <= .3 && karma >= 0) {
      label = 'warning';
      message = 'Fair';
    } else if (karma < 0 && karma >= -.4) {
      label = 'danger';
      message = 'Bad';
    } else {
      label = 'danger';
      message = 'Very bad';
    }

    return [label, message];
  }

  render() {
    const marker = this.getSentimentMarker(this.props.karma);
    const label = marker[0], message = marker[1];

    return (
      <ListGroupItem>
        <p>{this.props.text}</p>
        <Label bsStyle={label}>{message}</Label>
        <div className="review-control">
          <div className="review-control__sentiment">
            <MdDone
              onClick={this.markPositiveSentiment.bind(this)}
              size={24}/>
            <MdClear
              onClick={this.markNegativeSentiment.bind(this)}
              size={24}/>
          </div>
          <div
            className="review-control__spam"
            onClick={this.markAsSpam.bind(this)}>Mark as spam...</div>
        </div>
      </ListGroupItem>
    );
  }
}

ReviewModalItem.propTypes = {
  reviewId: PropTypes.string.isRequired,
  projectId: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
  karma: PropTypes.number
};

export default ReviewModalItem;