#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from Gondwana.model import db, Channel, Order
from pycscart import Cscart
import json

bp = Blueprint('order', __name__, url_prefix='/order')


# /order/index
@bp.route('/index', methods=('GET', ))
def order_index():
    channels = Channel.query.all()
    active_channel = None

    # get arguments
    channel_id = request.args.get('channel_id')

    # set Order query with filter
    # https://stackoverflow.com/questions/37336520/sqlalchemy-dynamic-filter
    orders_query = db.session.query(Order) # create Order Query
    if channel_id: # Add conditions
        orders_query = orders_query.filter(Order.channel_id==channel_id)
        active_channel = Channel.query.filter(Channel.id==channel_id).first()
    orders = orders_query.all() # execute Query

    return render_template('order/index.html', active_page="order_index", orders=orders, channels=channels, active_channel=active_channel)

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
                order.status = o['status']
            else:
                order = Order(
                        order_id=o['order_id'],
                        channel_id=channel.id,
                        status=o['status'])
                db.session.add(order)

            db.session.commit()
            current_app.logger.debug("Channel %s:Order %s updated!" % (channel.name, order_id))
        current_app.logger.info("Channel #%s updated!" % (channel.name))

    flash('Update Completed!', 'success')
    return redirect(url_for('order.order_index'))
