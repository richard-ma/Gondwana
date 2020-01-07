#!/usr/bin/env python
# encoding: utf-8

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fMHTYwNUABVwlf1ySV87n7Um5cEzL6Ir'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass

config={
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig,
        }
