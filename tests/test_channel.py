#!/usr/bin/env python
# encoding: utf-8

def test_empty_database(client):
    response = client.get('/channel/index')

    assert response.status_code == 200
    # confirm message
    assert b'No channels here.' in response.data
    # confirm Create Channel Button
    assert b'Create Channel</a>' in response.data

def test_channel_create_form(client):
    response = client.get('/channel/create')

    assert response.status_code == 200

    # confirm form
    assert b'inputName' in response.data
    assert b'inputWebsite' in response.data
    assert b'inputEmail' in response.data
    assert b'inputApikey' in response.data
    assert b'<button type="submit" class="btn btn-primary">Save</button>' in response.data

def test_create_channel(client):
    # test channel
    test_channel_data = dict(
        inputName='test_channel_name',
        inputWebsite='http://test_channel_website.com',
        inputEmail='test@test_channel.com',
        inputApikey='test_channel_api_key',
    )

    response = client.post(
            '/channel/create',
            data=test_channel_data,
            follow_redirects=True
            )

    # confirm flash message
    assert b'<strong>SUCCESS:</strong> <span>Channel has been created!</span>' in response.data

    # confirm channel information
    assert bytes(test_channel_data['inputName'], encoding='utf8') in response.data
    assert bytes(test_channel_data['inputWebsite'], encoding='utf8') in response.data
    assert bytes(test_channel_data['inputEmail'], encoding='utf8') in response.data
    assert bytes(test_channel_data['inputApikey'], encoding='utf8') in response.data

    # confirm operation button
    assert b'Edit</a>' in response.data
    assert b'Delete</a>' in response.data
