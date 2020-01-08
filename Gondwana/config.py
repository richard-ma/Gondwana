#!/usr/bin/env python
# encoding: utf-8

import os
from flask import current_app


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'fMHTYwNUABVwlf1ySV87n7Um5cEzL6Ir'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Gondwana-development.sqlite'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Gondwana-testing.sqlite'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Gondwana-production.sqlite'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
