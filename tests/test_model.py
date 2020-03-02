#!/usr/bin/env python
# encoding: utf-8
'''
def test_init_db_command(runner, monkeypatch):
    class Recorder():
        called = False

    def fake_create_all():
        Recorder.called = True

    monkeypatch.setattr('Gondwana.model.db.create_all', fake_create_all)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized the database.' in result.output
    assert Recorder.called
'''
