#!/usr/bin/env python
# encoding: utf-8

import pytest
from flask_script import Manager
from flask_migrate import MigrateCommand
from Gondwana import create_app

app = create_app()

# initial manager instance
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    pytest.main(["-s", "tests"])

if __name__ == "__main__":
    manager.run()
