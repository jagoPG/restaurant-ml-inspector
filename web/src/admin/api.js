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

import axios from 'axios';

const AXIOS_CONFIG = {
  headers: {'X-Requested-With': 'XMLHttpRequest'},
};


const requestGetProjects = (onSuccess) => {
  return axios.get('/admin/projects/', AXIOS_CONFIG)
    .then((response) => {
      onSuccess(response.data)
    });
};

const requestGetProject = ({projectId}, onSuccess) => {
  return axios.get(`/api/project/${projectId}/`)
    .then((response) => {
      onSuccess(response.data);
    });
};

const requestGetProjectDetails = ({projectId}, onSuccess) => {
  return axios.get(`/api/project/details/${projectId}/`)
    .then((response) => {
      onSuccess(response.data);
    });
};

const requestGetProjectDataSources = ({projectId}, onSuccess) => {
  return axios.get(`/api/project/sources/${projectId}/`)
    .then((response) => {
      onSuccess(response.data);
    });
};

const requestGetRestaurantNetworkIdentifier = ({country, name, network}, onSuccess, onError) => {
  return axios.get(`/api/sources/?name=${name}&network=${network}&country=${country}`, AXIOS_CONFIG)
    .then((response) => {
      onSuccess(response.data);
    }).catch((err) => {
      onError(err.response.data, err.response.status);
    });
};

const requestGetCountries = (onSuccess) => {
  return axios.get('/api/country/', AXIOS_CONFIG)
    .then((response) => {
      onSuccess(response.data);
    })
};

const requestUsers = (onSuccess) => {
  return axios.get('/admin/users/', AXIOS_CONFIG).then((response) => {
    onSuccess(response.data);
  })
};

const activateUser = (userIdentifier, onSuccess, onError) => {
  return axios.put(`/admin/user/activate/${userIdentifier}/`, null, AXIOS_CONFIG)
    .then((response) => {
      onSuccess ? onSuccess(response.data) : null;
    }).catch((error) => {
      onError ? onError(error) : null;
    })
};

const deactivateUser = (userIdentifier, onSuccess, onError) => {
  return axios.put(`/admin/user/deactivate/${userIdentifier}/`, null, AXIOS_CONFIG)
    .then((response) => {
      onSuccess ? onSuccess(response.data) : null;
    }).catch((error) => {
      onError ? onError(error) : null;
    })
};

const updateUserRoles = ({userIdentifier, roles}, onSuccess, onError) => {
  return axios.put(`/admin/user/roles/${userIdentifier}/`, {roles}, AXIOS_CONFIG)
    .then((response) => {
      onSuccess ? onSuccess(response.data) : null;
    }).catch((error) => {
      onError ? onError(error) : null;
    })
};

const createProject = ({name, description}, onSuccess) => {
  return axios.post('/admin/project/', {name, description}, AXIOS_CONFIG)
    .then(() => {
      onSuccess ? onSuccess() : null;
    });
};

const editProject = ({projectId, name, description}, onSuccess) => {
  return axios.put(`/admin/project/${projectId}/`, {name, description}, AXIOS_CONFIG)
    .then(() => {
      onSuccess ? onSuccess() : null;
    });
};

const deleteProject = ({projectId}, onSuccess) => {
  return axios.delete(`/admin/project/${projectId}/`, AXIOS_CONFIG)
    .then(() => {
      onSuccess ? onSuccess() : null;
    });
};

const addDataSource = ({social_network, restaurant_id, country, geo_position, project_id}, onSuccess) => {
  let args = {
    social_network, restaurant_id
  };
  if (country) {
    args.country = country;
  }
  if (geo_position) {
    args.geo_position = geo_position;
  }
  return axios.post(`/admin/project/sources/${project_id}/`, args, AXIOS_CONFIG)
    .then(() => {
      onSuccess ? onSuccess() : null;
    });
};

const editDataSource = ({social_network, restaurant_id, country, geo_position, project_id}, onSuccess) => {
  let args = {
    social_network, restaurant_id
  };
  if (country) {
    args.country = country;
  }
  if (geo_position) {
    args.geo_position = geo_position;
  }
  return axios.put(`/admin/project/sources/${project_id}/`, args, AXIOS_CONFIG)
    .then(() => {
      onSuccess ? onSuccess() : null;
    });
};

const retrieveDataFromSocialNetworks = ({projectId}, onSuccess, onError) => {
  return axios.put(`/admin/project/retrieve-data/${projectId}/`, null, AXIOS_CONFIG)
    .then(() => {
      onSuccess ? onSuccess() : null;
    }).catch(() => {
      onError ? onError() : null;
    });
};

const requestAnalysis = ({projectId}, onSuccess, onError) => {
  return axios.put(`/admin/project/analyse/${projectId}/`, null, AXIOS_CONFIG)
    .then(() => {
      onSuccess ? onSuccess() : null;
    }).catch(() => {
      onError ? onError() : null;
    });
};

const markReviewAsSpam = ({project_id, review_id, is_spam}, onSuccess) => {
  return axios.put(`/admin/project/${project_id}/review/${review_id}/spam/`, {
    is_spam
  }, AXIOS_CONFIG).then(() => {
    onSuccess ? onSuccess() : null;
  });
};

const editReviewSentiment = ({project_id, review_id, sentiment}, onSuccess) => {
  return axios.put(`/admin/project/${project_id}/review/${review_id}/sentiment/`, {
    sentiment
  }, AXIOS_CONFIG).then(() => {
    onSuccess ? onSuccess() : null;
  });
};

export {
  requestGetProjects,
  requestGetProject,
  requestGetProjectDetails,
  requestGetRestaurantNetworkIdentifier,
  requestGetProjectDataSources,
  createProject,
  editProject,
  addDataSource,
  editDataSource,
  deleteProject,
  retrieveDataFromSocialNetworks,
  requestAnalysis,
  requestGetCountries,
  requestUsers,
  updateUserRoles,
  activateUser,
  deactivateUser,
  markReviewAsSpam,
  editReviewSentiment
};
