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
import {debounce} from 'throttle-debounce';
import MapItem from './MapItem';
import RestaurantModal from './RestaurantModal';
import './MapArea.scss';

class MapArea extends Component {
  constructor(props) {
    super(props);
    this.state = {
      width: 500,
      projectId: null
    };
    this.updateWindowDimensions = debounce(200, true, this.updateWindowDimensions.bind(this));
  }

  onRestaurantClicked(projectId) {
    this.setState({projectId});
  }

  clearRestaurantClicked() {
    this.setState({projectId: null});
  }

  componentDidMount() {
    this.updateWindowDimensions();
    window.addEventListener('resize', this.updateWindowDimensions);
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.updateWindowDimensions);
  }

  updateWindowDimensions() {
    this.setState({
      width: window.innerWidth,
    });
  }

  render() {
    return (
      <div>
        <div className='map_container'>
          <MapItem
            width={this.state.width*0.8}
            onRestaurantClicked={this.onRestaurantClicked.bind(this)}/>
        </div>
        <RestaurantModal
          projectId={this.state.projectId}
          clearRestaurantClicked={this.clearRestaurantClicked.bind(this)}/>
      </div>
    );
  }
}

export default MapArea;