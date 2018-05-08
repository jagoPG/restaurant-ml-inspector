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
import PropTypes from 'prop-types';
import TiEdit from 'react-icons/lib/ti/edit';
import MdDelete from 'react-icons/lib/md/delete';
import MdDetails from 'react-icons/lib/md/details';

class ProjectListFormItem extends Component {
  constructor(props) {
    super(props);
    this.dispatchSelectProject = this.dispatchSelectProject.bind(this);
  }

  onDeleteClicked() {
    this.props.onDeleteButtonClicked(this.props.projectIdentifier, this.props.projectName);
  }

  dispatchSelectProject() {
    this.props.store.dispatch({
      type: 'VIEW_PROJECT', projectId: this.props.projectIdentifier, projectName: null
    });
  }

  render() {
    const style = {
      color: 'black',
    };
    const
      editPageLink = `/admin/project/edit/${this.props.projectIdentifier}/`,
      detailsPageLink = `/admin/project/${this.props.projectIdentifier}/`;

    return (
      <tr>
        <td>{this.props.projectName}</td>
        <td>{this.props.projectCreatedOn}</td>
        <td>
          <Link to={editPageLink}>
            <TiEdit style={style} size={28} onClick={this.dispatchSelectProject}/>
          </Link>
          <MdDelete onClick={this.onDeleteClicked.bind(this)} size={28}/>
          <Link to={detailsPageLink}>
            <MdDetails style={style} size={28} onClick={this.dispatchSelectProject}/>
          </Link>
        </td>
      </tr>
    );
  }
}

ProjectListFormItem.propTypes = {
  projectName: PropTypes.string.isRequired,
  projectCreatedOn: PropTypes.string,
  projectIdentifier: PropTypes.string.isRequired,
  onDeleteButtonClicked: PropTypes.func.isRequired,
  store: PropTypes.object.isRequired,
};

export default ProjectListFormItem;