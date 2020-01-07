#!/usr/bin/env python
# encoding: utf-8

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fMHTYwNUABVwlf1ySV87n7Um5cEzL6Ir'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLACHEMY_DATABASE_URI = ''

class TestingConfig(Config):
    TESTING = True
    SQLACHEMY_DATABASE_URI = ''

class ProductionConfig(Config):
    SQLACHEMY_DATABASE_URI = ''

config={
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig,
        }
