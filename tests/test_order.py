#!/usr/bin/env python
# encoding: utf-8

def test_empty_database(client):
    response = client.get('/order/index')

    assert response.status_code == 200
    # confirm message
    #assert b'No orders here.' in response.data
    # confirm Create Channel Button
    #assert b'Update</a>' in response.data
