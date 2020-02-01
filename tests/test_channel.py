#!/usr/bin/env python
# encoding: utf-8

def test_empty_database(client):
    response = client.get('/channel/index')
    response_data = str(response.data)

    assert response.status_code == 200
    # confirm message
    assert 'No channels here.' in response_data
    # confirm Create Channel Button
    assert 'Create Channel</a>' in response_data
