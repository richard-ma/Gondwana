#!/usr/bin/env python
# encoding: utf-8

def test_true():
    assert True

def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.data == b'pong'
