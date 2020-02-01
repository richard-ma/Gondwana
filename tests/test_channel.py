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

def test_channel_create_form(client):
    response = client.get('/channel/create')
    response_data = str(response.data)

    assert response.status_code == 200

    # confirm form
    assert 'inputName' in response_data
    assert 'inputWebsite' in response_data
    assert 'inputEmail' in response_data
    assert 'inputApikey' in response_data
    assert '<button type="submit" class="btn btn-primary">Save</button>' in response_data
