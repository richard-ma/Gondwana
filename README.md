# Gondwana
[![Build Status](https://www.travis-ci.org/richard-ma/Gondwana.svg?branch=master)](https://www.travis-ci.org/richard-ma/Gondwana)

## INSTALL

* sudo apt-get install mysql-server libmysqlclient-dev
* pip install -r requirements.txt
* [EDIT] /config/config-production.cfg [SQLALCHEMY_DATABASE_URI]
* [COPY] /config/config-production.cfg => [INSTANCE FOLDER]
* ./manager db init
* ./manager db migrate
* ./manager db upgrade

## RUN

* ./script-run-production.sh

# ./script-run-production.sh

## cscart CLI Testing tool

### Testing API connection
curl --user admin@example.com:APIkey -X GET 'http://example.com/api/users/'

# References

* [CS-cart REST API](https://docs.cs-cart.com/latest/developer_guide/api/index.html#)
