#!/usr/bin/env python
# encoding: utf-8

import os, shutil
from flask import Flask


def create_app(conf=None):
    app = Flask(__name__, instance_relative_config=True)

    from . import jinja_filters
    app.register_blueprint(jinja_filters.bp)
    app.logger.debug('Add jinja_filters blueprint')

    # check instance folder
    if os.path.isdir(app.instance_path):
        app.logger.debug('Instance path folder exists.')
    else:
        # create instance path folder
        os.makedirs(app.instance_path)
        app.logger.warning('Instance path folder not exists. Create New!')

    # Get Flask ENV
    e = os.environ.get('FLASK_ENV', 'production')

    # config logger
    import logging
    from logging.handlers import RotatingFileHandler
    from flask.logging import default_handler

    if e == 'development':
        rotating_filename = 'development.log'
        log_level = logging.DEBUG
    else:
        rotating_filename = 'production.log'
        log_level = logging.WARNING

    rotating_file_handler = RotatingFileHandler(os.path.join(
        app.instance_path, rotating_filename),
                                                maxBytes=2000000,
                                                backupCount=10)

    for logger in (app.logger, logging.getLogger('sqlalchemy.engine')):
        logger.addHandler(default_handler)
        logger.addHandler(rotating_file_handler)
        logger.setLevel(log_level)

    # Cann't find config.cfg in instance path
    config_filename = 'config-%s.cfg' % (e)
    if not os.path.isfile(os.path.join(app.instance_path, config_filename)):
        app.logger.warning('Create %s file in instance folder' %
                           (config_filename))
        from shutil import copyfile
        copyfile(os.path.join('config', config_filename),
                 os.path.join(app.instance_path, config_filename))

    # load config.cfg
    app.config.from_pyfile(config_filename, silent=True)

    # check upload folder
    upload_path = os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'])

    if os.path.isdir(upload_path):
        app.logger.debug('Upload path folder exists.')
    else:
        # create upload folder
        os.mkdirs(upload_path)
        app.logger.warning('Upload path folder not exists. Create New!')
    # clear upload folder
    for filename in os.listdir(upload_path):
        file_path = os.path.join(upload_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                app.logger.debug('Delete: %s' % (file_path))
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                app.logger.debug('Delete: %s' % (file_path))
        except Exception as e:
            app.logger.warning('Failed to delete %s. Reason: %s' % (file_path, e))
    # check upload folder empty or not
    if os.path.isdir(upload_path) and len(os.listdir(upload_path)) == 0:
        app.logger.debug('All files in upload folder have been deleted.')
    else:
        app.logger.debug('Upload folder is not empty.')

    # SQLALCHEMY_DATABASE_URI
    app.logger.debug('SQLALCHEMY_DATABASE_URI: %s' %
                     (app.config['SQLALCHEMY_DATABASE_URI']))

    # refresh config with conf parameter
    if conf is not None:
        app.config.from_mapping(conf)

    # import helper function
    from . import helper

    # register template helper
    app.add_template_global(helper.get_all_order_status, name="get_all_order_status")
    app.add_template_global(helper.get_all_shipping_methods, name="get_all_shipping_methods")
    app.logger.debug('Load helpers')

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

    from . import api
    app.register_blueprint(api.bp)
    app.logger.debug('Add api blueprint')

    from . import dashboard
    app.register_blueprint(dashboard.bp)
    app.logger.debug('Add dashboard blueprint')

    from . import channel
    app.register_blueprint(channel.bp)
    app.logger.debug('Add channel blueprint')

    from . import order
    app.register_blueprint(order.bp)
    app.logger.debug('Add order blueprint')

    return app
