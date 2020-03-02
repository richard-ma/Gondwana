#!/usr/bin/env python
# encoding: utf-8

import os
from flask import Flask


def create_app(conf=None):
    app = Flask(__name__, instance_relative_config=True)

    config_type = os.environ.get('FLASK_ENV', default="development")
    app.logger.debug('config_type: %s' % (config_type))

    app.config.from_object('config.' + config_type)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_pyfile('config.py', silent=True)

    if conf is not None:
        app.config.from_mapping(conf)

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
