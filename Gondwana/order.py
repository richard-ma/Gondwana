#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from Gondwana.model import db, Channel, Order
from pycscart import Cscart
import json

bp = Blueprint('order', __name__, url_prefix='/order')


# /order/index
@bp.route('/index', methods=('GET', 'POST'))
def order_index():
    channels = Channel.query.all()
    orders = None
    active_channel = None
    active_status = None

    if request.method == 'GET':
        # get arguments
        channel_id = request.args.get('channel_id')
        status = request.args.get('status')

        # set Order query with filter
        # https://stackoverflow.com/questions/37336520/sqlalchemy-dynamic-filter
        orders_query = db.session.query(Order)  # create Order Query
        if channel_id:  # Add conditions
            orders_query = orders_query.filter(Order.channel_id == channel_id)
            active_channel = Channel.query.filter(
                Channel.id == channel_id).first()
        if status:  # status filter
            orders_query = orders_query.filter(Order.status == status)
            active_status = status
        orders = orders_query.all()  # execute Query

    if request.method == 'POST':  # search
        order_id = request.form.get('order_id')

        orders = Order.query.filter(Order.order_id == order_id).all()

    return render_template('order/index.html',
                           active_page="order_index",
                           orders=orders,
                           channels=channels,
                           active_channel=active_channel,
                           active_status=active_status)


# /order/sync
@bp.route('/sync', methods=('GET', ))
def order_sync():
    for channel in Channel.query.all():
        api = Cscart(channel.website_url, channel.email, channel.api_key)
        response = api.get_orders()
        for o in response['orders']:
            order_id = o['order_id']
            order_remote = api.get_order(order_id)
            order_local = Order.query.filter(Order.order_id == order_id).first()
            if order_local:
                order_local.order_id = order_id
                order_local.channel_id = channel.id
                order_local.status = order_remote['status']

                # customer information
                order_local.firstname = order_remote['firstname']
                order_local.lastname = order_remote['lastname']
                order_local.phone = order_remote['phone']
                order_local.fax = order_remote['fax']
                order_local.url = order_remote['url']
                order_local.email = order_remote['email']
                order_local.ip_address = order_remote['ip_address']
            else:
                order = Order(order_id=order_remote['order_id'],
                              channel_id=channel.id,
                              status=order_remote['status'],
                              firstname=order_remote['firstname'],
                              lastname=order_remote['lastname'],
                              phone=order_remote['phone'],
                              fax=order_remote['fax'],
                              url=order_remote['url'],
                              email=order_remote['email'],
                              ip_address=order_remote['ip_address'])
                db.session.add(order)
            current_app.logger.debug("Channel %s:Order %s synchronized!" %
                                     (channel.name, order_id))
        db.session.commit()
        current_app.logger.info("Channel #%s synchronized!" % (channel.name))

    flash('Synchronization Completed!', 'success')
    return redirect(url_for('order.order_index'))


# /order/updat_estatus/<str:channel_id>/<str:order_id>/<str:status>
@bp.route(
    '/update_status/<string:channel_id>/<string:order_id>/<string:status>',
    methods=('GET', ))
def order_update_status(channel_id: str, order_id: str, status: str):
    order = Order.query.filter(Order.id == order_id).filter(
        Order.channel_id == channel_id).first()
    channel = order.channel

    api = Cscart(channel.website_url, channel.email, channel.api_key)
    response = api.update_order_status(str(order.order_id), status)

    if response:
        order.status = status
        db.session.commit()
        flash('Update Order Status Completed', 'success')
        current_app.logger.debug("Channel #%s Order #%s status change to %s" %
                                 (channel.name, order.id, order.status))

    return redirect(url_for('order.order_index'))
