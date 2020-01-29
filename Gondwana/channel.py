#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, current_app

bp = Blueprint('channel', __name__, url_prefix='/channel')


# /channel/index
@bp.route('/index', methods=('GET', 'POST'))
def channel_index():
    if request.method == 'POST':
        pass

    return render_template('channel/index.html', active_page="channel_index")


# /channel/create
@bp.route('/create', methods=('GET', 'POST'))
def channel_create():
    if request.method == 'POST':
        current_app.logger.debug('create channel')

        return redirect(url_for('channel.channel_index'))

    return render_template('channel/create.html')


# /channel/delete/<str:id>
@bp.route('/delete/<string:id>', methods=('GET', 'POST'))
def channel_delete(id: str):
    if request.method == 'POST':
        pass

    return redirect(url_for('channel.channel_index'))


# /channel/update/<int:id>
@bp.route('/update/<string:id>', methods=('GET', 'POST'))
def channel_update(id: str):
    if request.method == 'POST':
        pass

    return render_template('channel/update.html')


# /channel/info/<int:id>
@bp.route('/info/<string:id>', methods=('GET', 'POST'))
def channel_info(id: str):
    if request.method == 'POST':
        pass

    return render_template('channel/info.html')
