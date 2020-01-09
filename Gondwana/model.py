#!/usr/bin/env python
# encoding: utf-8

import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# models
class Channel(db.Model):
    __tablename__ = 'channel'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    website_url = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), nullable=False)
    api_key = db.Column(db.String(128), nullable=False)

    def __init__(self, name, website_url, email, api_key):
        self.name = name
        self.website_url = website_url
        self.email = email
        self.api_key = api_key

# command line
@click.command('init-db')
@with_appcontext
def init_db_command():
    db.create_all()
    click.echo('Initialized the database.')
