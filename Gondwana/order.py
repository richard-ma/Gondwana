#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request

bp = Blueprint('order', __name__, url_prefix='/order')


# /order/index
@bp.route('/index', methods=('GET', 'POST'))
def order_index():
    if request.method == 'POST':
        pass

    return render_template('order/index.html', active_page="order_index")

# /order/update
@bp.route('/update', methods=('GET',))
def order_update():
    orders = []

    return render_template('order/index.html', active_page="order_index", orders=orders)
