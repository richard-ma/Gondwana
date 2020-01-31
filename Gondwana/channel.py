#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, current_app
from Gondwana.model import db, Channel

bp = Blueprint('channel', __name__, url_prefix='/channel')


# /channel/index
@bp.route('/index', methods=('GET',))
def channel_index():
    channels = Channel.query.all()

    return render_template('channel/index.html', active_page="channel_index", channels=channels)


# /channel/create
@bp.route('/create', methods=('GET', 'POST'))
def channel_create():
    if request.method == 'POST':
        current_app.logger.debug('create channel')

        # get parameters
        name = request.form['inputName']
        website = request.form['inputWebsite']
        email = request.form['inputEmail']
        apiKey = request.form['inputApikey']
        current_app.logger.debug('name: %s' % (name))
        current_app.logger.debug('website: %s' % (website))
        current_app.logger.debug('email: %s' % (email))
        current_app.logger.debug('apiKey: %s' % (apiKey))

        # create Channel object
        channel = Channel(name, website, email, apiKey)
        current_app.logger.debug('channel: %s/%s/%s/%s' % (
            channel.name,
            channel.website_url,
            channel.email,
            channel.api_key,
        ))

        # save to database
        db.session.add(channel)
        db.session.commit()

        return redirect(url_for('channel.channel_index'))

    return render_template('channel/create.html')


# /channel/delete/<str:id>
@bp.route('/delete/<string:id>', methods=('GET',))
def channel_delete(id: str):
    current_app.logger.debug("Delete #%s Channel" % (id))

    # query the record
    channel = Channel.query.filter_by(id=id).first()
    current_app.logger.debug("Queried Channel id: %s" % (id))

    # save to database
    db.session.delete(channel)
    db.session.commit()

    return redirect(url_for('channel.channel_index'))


# /channel/update/<int:id>
@bp.route('/update/<string:id>', methods=('GET', 'POST'))
def channel_update(id: str):
    channel = Channel.query.filter_by(id=id).first()
    current_app.logger.debug("Queried Channel id: %s" % (channel.id))

    if request.method == 'POST':
        current_app.logger.debug('update channel #%s' % (channel.id))

        # get parameters
        channel.name = request.form['inputName']
        channel.website_url = request.form['inputWebsite']
        channel.email = request.form['inputEmail']
        channel.api_key = request.form['inputApikey']
        current_app.logger.debug('name: %s' % (channel.name))
        current_app.logger.debug('website: %s' % (channel.website_url))
        current_app.logger.debug('email: %s' % (channel.email))
        current_app.logger.debug('apiKey: %s' % (channel.api_key))

        db.session.commit()

    return render_template('channel/update.html', channel=channel)


# /channel/info/<int:id>
@bp.route('/info/<string:id>', methods=('GET', 'POST'))
def channel_info(id: str):
    if request.method == 'POST':
        pass

    return render_template('channel/info.html')
