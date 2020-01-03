#!/usr/bin/env python
# encoding: utf-8

import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/ping')
    def ping():
        return 'pong'

    from . import channel
    app.register_blueprint(channel.bp)

    from . import order
    app.register_blueprint(order.bp)

    return app
