#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request

bp = Blueprint('order', __name__, url_prefix='/order')


# /order/index
@bp.route('/index', methods=('GET', 'POST'))
def channel_index():
    if request.method == 'POST':
        pass

    return render_template('order/index.html')
