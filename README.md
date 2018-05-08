[![Build Status](https://travis-ci.com/jagoPG/pfm-web-application.svg?token=CcawYx3eF4wps3ZDbkyn&branch=master)](https://travis-ci.com/jagoPG/pfm-web-application)

# MASTER THESIS WEB APPLICATION # 
This project follows a *SaaS* architecture for providing analytical services
to two different stakeholders. Offers to restaurant owners a tool for getting
an analysis of the social opinion of their business. And provides to citizens
a tool for letting them know about the restaurant ratings on their surroundings.

For achieving this, social networks data, an other available Open Data sources
on the Web are queried. Multi-language user opinions and other unstructured data
about the products and services of a restaurant business are obtained and
processed through different semantic analysis techniques. The data is stored as
a new graph model which is adapted to the channel of the stakeholder.

## Required applications ##
- Neo4j
- Python 3.x
- Python `VirtualEnv`

## Setup ##
1. Create a virtual environment for installing and executing the application:
```shell
$ virtualenv -p /usr/local/bin/python3 venv
```

2. Create a `load_config.sh` file from the template `load_config_sh.dist` and fill the variables 
with your development credentials.

3 Load the virtual environment and set variables:
```shell
$ source venv/bin/activate
$ source bin/load_config.sh
```

4. Install the libraries from the `requirements.txt` file:
```shell
$ pip3 install -r requirements.txt
```

5. Execute `main.py` file.

## Deploy ##
All variables of the `bin/load_config.sh.dist` file have to be set up in the server. Furthermore, 
**Textblob** corpora has to be downloaded, as the `bin/install_textblob_corpora` file suggests.

```
$ git push heroku master
```

## Integration Tests ##
Before executing the tests, some information will be loaded into the database. So, do not launch
the tests on a production server because it could lead to data loss.

```shell
## Stop database
$ brew services stop neo4j

## Prepare environment
$ rm -r $NEO4J_HOME/libexec/data/databases/<DB_NAME>
$ neo4j-admin load --from=test/test_database.backup --database=<DB_NAME>

## Start database
$ brew services start neo4j

## Launch tests
$ python tests.py -v
```

The Integration Tests can be executed along with a code coverage test. The following commands will
execute the integration tests. After that, a report with the code coverage of the application will
be shown.

```shell
$ coverage run tests.py -v
$ coverage html
```

## About ##
Jagoba P. G. <jagobaperez92@opendeusto.es> | https://jagobapg.eu
