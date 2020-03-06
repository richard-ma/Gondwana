#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request
from Gondwana.model import db, Channel, Order
from pycscart import Cscart
import json

bp = Blueprint('order', __name__, url_prefix='/order')


# /order/index
@bp.route('/index', methods=('GET', ))
def order_index():
    orders = Order.query.all()
    channels = Channel.query.all()

    return render_template('order/index.html', active_page="order_index", orders=orders, channels=channels)

# /order/update
@bp.route('/update', methods=('GET',))
def order_update():
    orders = []

    for channel in Channel.query.all():
        api = Cscart(channel.website_url, channel.email, channel.api_key)
        response = api.get_orders()
        for o in response['orders']:
            order_id = o['order_id']
            order = Order.query.filter(Order.order_id==order_id).first()
            if order:
                order.order_id = order_id
                order.channel_id = channel.id
            else:
                order = Order(
                        order_id=o['order_id'],
                        channel_id=channel.id)
                db.session.add(order)

            db.session.commit()

    return redirect(url_for('order.order_index'))
