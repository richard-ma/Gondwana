#!/usr/bin/env python
# encoding: utf-8

import json
from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from Gondwana.model import db, Channel, Order
from pycscart import Cscart
from sqlalchemy import or_

bp = Blueprint('order', __name__, url_prefix='/order')


# /order/index
@bp.route('/index', methods=('GET', 'POST'))
def order_index():
    channels = Channel.query.all() # get all channels
    orders_query = db.session.query(Order)  # create Order Query
    active_channel = None
    active_status = None
    keyword = None

    if request.method == 'POST':  # search or batch
        # get arguments
        keyword = request.form.get('keyword')
        channel_id = request.form.get('channel_id')
        status = request.form.get('status')
        status_to = request.form.get('status_to')

        # set Order query with filter
        # https://stackoverflow.com/questions/37336520/sqlalchemy-dynamic-filter
        # search
        if channel_id:  # Add conditions
            orders_query = orders_query.filter(Order.channel_id == channel_id)
            active_channel = Channel.query.filter(Channel.id == channel_id).first()
        if status:  # status filter
            orders_query = orders_query.filter(Order.status == status)
            active_status = status
        if keyword: # search keyword
            orders_query = orders_query.filter(or_(Order.order_id == keyword, Order.email == keyword))
        # batch
        if status_to: # change order status
            order_ids = request.form.get('order_ids')
            if order_ids:
                order_ids = [int(x) for x in order_ids.split(',')] # change string to integer
            # https://stackoverflow.com/questions/15267755/query-for-multiple-values-at-once
            batching_orders = Order.query.filter(Order.id.in_(order_ids))

    orders = orders_query.all()  # execute Query

    return render_template('order/index.html',
                           active_page="order",
                           orders=orders,
                           channels=channels,
                           active_channel=active_channel,
                           active_status=active_status,
                           keyword=keyword)

# /order/detail
@bp.route('/detail/<string:order_id>', methods=('GET', ))
def order_detail(order_id: str):
    order = Order.query.filter(Order.id==order_id).first()

    return render_template('/order/detail.html', order=order)

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

                # bill information
                order_local.b_firstname = order_remote['b_firstname']
                order_local.b_lastname = order_remote['b_lastname']
                order_local.b_address = order_remote['b_address']
                order_local.b_address_2 = order_remote['b_address_2']
                order_local.b_city = order_remote['b_city']
                order_local.b_county = order_remote['b_county']
                order_local.b_state = order_remote['b_state']
                order_local.b_country = order_remote['b_country']
                order_local.b_zipcode = order_remote['b_zipcode']
                order_local.b_phone = order_remote['b_phone']
                order_local.b_country_descr = order_remote['b_country_descr']
                order_local.b_state_descr = order_remote['b_state_descr']

                # shipping information
                order_local.s_firstname = order_remote['s_firstname']
                order_local.s_lastname = order_remote['s_lastname']
                order_local.s_address = order_remote['s_address']
                order_local.s_address_2 = order_remote['s_address_2']
                order_local.s_city = order_remote['s_city']
                order_local.s_county = order_remote['s_county']
                order_local.s_state = order_remote['s_state']
                order_local.s_country = order_remote['s_country']
                order_local.s_zipcode = order_remote['s_zipcode']
                order_local.s_phone = order_remote['s_phone']
                order_local.s_address_type = order_remote['s_address_type']
                order_local.s_country_descr = order_remote['s_country_descr']
                order_local.s_state_descr = order_remote['s_state_descr']
            else:
                order = Order(order_id=order_remote['order_id'],
                              channel_id=channel.id,
                              status=order_remote['status'],

                              # customer information
                              firstname=order_remote['firstname'],
                              lastname=order_remote['lastname'],
                              phone=order_remote['phone'],
                              fax=order_remote['fax'],
                              url=order_remote['url'],
                              email=order_remote['email'],
                              ip_address=order_remote['ip_address'],

                              # bill information
                              b_firstname=order_remote['b_firstname'],
                              b_lastname=order_remote['b_lastname'],
                              b_address=order_remote['b_address'],
                              b_address_2=order_remote['b_address_2'],
                              b_city=order_remote['b_city'],
                              b_county=order_remote['b_county'],
                              b_state=order_remote['b_state'],
                              b_country=order_remote['b_country'],
                              b_zipcode=order_remote['b_zipcode'],
                              b_phone=order_remote['b_phone'],
                              b_country_descr=order_remote['b_country_descr'],
                              b_state_descr=order_remote['b_state_descr'],

                              # shipping information
                              s_firstname=order_remote['s_firstname'],
                              s_lastname=order_remote['s_lastname'],
                              s_address=order_remote['s_address'],
                              s_address_2=order_remote['s_address_2'],
                              s_city=order_remote['s_city'],
                              s_county=order_remote['s_county'],
                              s_state=order_remote['s_state'],
                              s_country=order_remote['s_country'],
                              s_zipcode=order_remote['s_zipcode'],
                              s_phone=order_remote['s_phone'],
                              s_address_type=order_remote['s_address_type'],
                              s_country_descr=order_remote['s_country_descr'],
                              s_state_descr=order_remote['s_state_descr']
                )
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

    #api = Cscart(channel.website_url, channel.email, channel.api_key)
    #response = api.update_order_status(str(order.order_id), status)

    order.status = status
    db.session.commit()

    flash('Update Order Status Completed', 'success')
    current_app.logger.debug("Channel #%s Order #%s status change to %s" %
                             (channel.name, order.id, order.status))

    return redirect(url_for('order.order_index'))
