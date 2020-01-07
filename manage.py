#!/usr/bin/env python
# encoding: utf-8

import pytest
from flask_script import Manager
from Gondwana import create_app

app = create_app()

# initial manager instance
manager = Manager(app)

@manager.command
def test():
    pytest.main(["-s", "Gondwana/tests"])

if __name__ == "__main__":
    manager.run()
