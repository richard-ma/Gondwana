#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from Gondwana.model import db, Channel
from sqlalchemy import or_

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
        # get parameters
        data = dict()
        data['name'] = request.form['inputName']
        data['website_url'] = request.form['inputWebsite']
        data['email'] = request.form['inputEmail']
        data['api_key'] = request.form['inputApikey']

        if data['name'] and data['website_url'] and data['email'] and data['api_key']:
            existing_channel = Channel.query \
                    .filter(or_(Channel.name==data['name'], Channel.website_url==data['website_url'])) \
                    .first()
            if existing_channel:
                flash('Channel already existed.', 'warning')
            else:
                # create Channel object
                channel = Channel(**data)

                # save to database
                db.session.add(channel)
                db.session.commit()

                flash('Channel has been created!', 'success')
                return redirect(url_for('channel.channel_index'))
        else:
            flash('Any option MUST NOT be blank', 'warning')

    return render_template('channel/create.html')


# /channel/delete/<str:id>
@bp.route('/delete/<string:id>', methods=('GET',))
def channel_delete(id: str):
    # query the record
    channel = Channel.query.filter_by(id=id).first()

    # save to database
    db.session.delete(channel)
    db.session.commit()

    flash('Channel has been deleted!', 'success')
    return redirect(url_for('channel.channel_index'))


# /channel/update/<int:id>
@bp.route('/update/<string:id>', methods=('GET', 'POST'))
def channel_update(id: str):
    channel = Channel.query.filter_by(id=id).first()

    if request.method == 'POST':

        # get parameters
        channel.name = request.form['inputName']
        channel.website_url = request.form['inputWebsite']
        channel.email = request.form['inputEmail']
        channel.api_key = request.form['inputApikey']

        db.session.commit()

        flash('Channel update completed!', 'success')

    return render_template('channel/update.html', channel=channel)


# /channel/info/<int:id>
@bp.route('/info/<string:id>', methods=('GET', 'POST'))
def channel_info(id: str):
    if request.method == 'POST':
        pass

    return render_template('channel/info.html')
