#!/usr/bin/env python
# encoding: utf-8

import os
import pytest

from Gondwana import create_app


@pytest.fixture
def app():
    # set env to testing
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
