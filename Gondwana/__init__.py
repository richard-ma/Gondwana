#!/usr/bin/env python
# encoding: utf-8

import os
from flask import Flask


def create_app(conf=None):
    app = Flask(__name__, instance_relative_config=True)

    # create instance path folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Get Flask ENV
    e = os.environ.get('FLASK_ENV', 'production')

    # config logger
    import logging
    from logging.handlers import RotatingFileHandler
    from flask.logging import default_handler

    if e == 'development':
        default_handler.setLevel(logging.DEBUG)
        rotating_file_handler = RotatingFileHandler(
                os.path.join(app.instance_path, 'development.log'),
                maxBytes=2000000,
                backupCount=10)
        rotating_file_handler.setLevel(logging.DEBUG)
    else:
        default_handler.setLevel(logging.WARNING)
        rotating_file_handler = RotatingFileHandler(
                os.path.join(app.instance_path, 'production.log'),
                maxBytes=2000000,
                backupCount=10)
        rotating_file_handler.setLevel(logging.DEBUG)

    for logger in (app.logger, logging.getLogger('sqlalchemy')):
        logger.addHandler(default_handler)
        logger.addHandler(rotating_file_handler)

    # Cann't find config.cfg in instance path
    if not os.path.isfile(os.path.join(app.instance_path, 'config.cfg')):
        app.logger.debug('Create config.cfg file in instance folder')
        from shutil import copyfile
        app.logger.debug('FLASK_ENV=%s' % (e))
        copyfile(os.path.join('config', 'config-%s.cfg' % (e)),
                 os.path.join(app.instance_path, 'config.cfg'))

    # load config.cfg
    app.config.from_pyfile('config.cfg', silent=True)

    # refresh config with conf parameter
    if conf is not None:
        app.config.from_mapping(conf)

    # SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % (os.path.join(
        app.config['BASEDIR'], 'db.sqlite'))
    app.logger.debug('SQLALCHEMY_DATABASE_URI: %s' %
                     (app.config['SQLALCHEMY_DATABASE_URI']))

    from . import model
    # create database
    model.db.init_app(app)
    app.logger.debug('Initialize db')
    # bind with migrate
    model.migrate.init_app(app, model.db)
    app.logger.debug('Initialize migrate')

    @app.route('/ping')
    def ping():
        return 'pong'

    app.logger.debug('Add /ping testing url')

    from . import channel
    app.register_blueprint(channel.bp)
    app.logger.debug('Add channel blueprint')

    from . import order
    app.register_blueprint(order.bp)
    app.logger.debug('Add order blueprint')

    return app
