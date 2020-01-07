#!/usr/bin/env python
# encoding: utf-8

import os
from flask import Flask
from .config import config


def create_app(conf=None):
    app = Flask(__name__, instance_relative_config=True)

    config_type = os.environ.get('FLASK_ENV') or 'default'
    app.config.from_object(config[config_type])
    app.config.from_mapping(
        # set DATABASE path
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(
            app.instance_path, 'Gondwana-' + config_type + '.sqlite'), )

    if conf is not None:
        app.config.from_mapping(conf)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import model
    # create database
    model.db.init_app(app)
    # bind with migrate
    #model.migrate.init_app(app, model.db)

    app.cli.add_command(model.init_db_command)

    @app.route('/ping')
    def ping():
        return 'pong'

    from . import channel
    app.register_blueprint(channel.bp)

    from . import order
    app.register_blueprint(order.bp)

    return app
