#!/usr/bin/env python
# encoding: utf-8

import os
import tempfile
import pytest

from Gondwana import create_app
from Gondwana.model import db


# create app
@pytest.fixture
def app():
    # creaate fake database
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_path,
    })

    # set env to testing
    app.config['TESTING'] = True

    # import test data
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

    # remove fake database
    os.close(db_fd)
    os.unlink(db_path)


# create test client
@pytest.fixture
def client(app):
    return app.test_client()


# create test command line runner
@pytest.fixture
def runner(app):
    return app.test_cli_runner()
