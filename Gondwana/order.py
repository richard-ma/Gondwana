#!/usr/bin/env python
# encoding: utf-8

import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash, send_file
from Gondwana.model import *
from Gondwana.helper import *
from pycscart import Cscart
from sqlalchemy import or_

bp = Blueprint('order', __name__, url_prefix='/order')


# /order/download
@bp.route('/download', methods=('POST', ))
def order_download():
    download = request.form.get('download')

    if download:  # download order
        order_ids = request.form.get('order_ids')
        if order_ids:
            order_ids = [int(x) for x in order_ids.split(',')
                         ]  # change string to integer
        # https://stackoverflow.com/questions/15267755/query-for-multiple-values-at-once
        batching_orders = Order.query.filter(Order.id.in_(order_ids))

    import xlsxwriter

    xlsx_filename = os.path.join(current_app.instance_path,
                                 current_app.config['ORDER_DOWNLOAD_FILENAME'])
    workbook = xlsxwriter.Workbook(xlsx_filename)
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, 'helo')

    workbook.close()

    # https://stackoverflow.com/questions/50086585/download-file-from-root-directory-using-flask
    return send_file(xlsx_filename, as_attachment=True)


# /order/index
@bp.route('/index', methods=('GET', 'POST'))
def order_index():
    channels = Channel.query.all()  # get all channels
    events = Event.query.all()  # get all events
    orders_query = db.session.query(Order)  # create Order Query
    active_channel = None
    active_status = None
    active_event = None
    keyword = None

    if request.method == 'POST':  # search or batch
        # get arguments
        keyword = request.form.get('keyword')
        channel_id = request.form.get('channel_id')
        status = request.form.get('status')
        event_id = request.form.get('event')
        status_to = request.form.get('status_to')

        # set Order query with filter
        # https://stackoverflow.com/questions/37336520/sqlalchemy-dynamic-filter
        # search
        if channel_id:  # Add conditions
            orders_query = orders_query.filter(Order.channel_id == channel_id)
            active_channel = Channel.query.filter(
                Channel.id == channel_id).first()
        if status:  # status filter
            orders_query = orders_query.filter(Order.status == status)
            active_status = status
        if event_id:  # event filter
            # https://stackoverflow.com/questions/6474989/sqlalchemy-filter-by-membership-in-at-least-one-many-to-many-related-table
            orders_query = orders_query.filter(
                Order.events.any(Event.id.in_([event_id])))
            active_event = Event.query.filter(Event.id == event_id).first()
        if keyword:  # search keyword
            orders_query = orders_query.filter(
                or_(Order.order_id == keyword, Order.email == keyword))
        # batch
        if status_to:  # change order status
            order_ids = request.form.get('order_ids')
            if order_ids:
                order_ids = [int(x) for x in order_ids.split(',')
                             ]  # change string to integer
            # https://stackoverflow.com/questions/15267755/query-for-multiple-values-at-once
            batching_orders = Order.query.filter(Order.id.in_(order_ids))
            for order in batching_orders:
                order.status = status_to
            db.session.commit()

    orders = orders_query.all()  # execute Query

    return render_template('order/index.html',
                           active_page="order",
                           orders=orders,
                           events=events,
                           channels=channels,
                           active_channel=active_channel,
                           active_status=active_status,
                           active_event=active_event,
                           keyword=keyword)


# /order/detail
@bp.route('/detail/<string:order_id>', methods=('GET', ))
def order_detail(order_id: str):
    order = Order.query.filter(Order.id == order_id).first()

    return render_template('/order/detail.html', order=order)


# /order/sync
@bp.route('/sync', methods=('GET', ))
def order_sync():
    order_keys = get_model_keys(Order)

    for channel in Channel.query.all():
        api = Cscart(channel.website_url, channel.email, channel.api_key)
        response = api.get_orders()
        for o in response['orders']:
            order_id = o['order_id']
            order_remote = api.get_order(order_id)
            order_local = Order.query.filter(
                Order.order_id == order_id).first()

            order_remote['shipping_method'] = order_remote['shipping'][0][
                'shipping']  # shipping method

            # choose keys in order_remote
            order_remote = {
                k: v
                for k, v in order_remote.items() if k in order_keys
            }
            order_remote['channel'] = channel  # add foreign key

            # timestamp to datetime
            # https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date
            order_remote['timestamp'] = datetime.utcfromtimestamp(
                int(order_remote['timestamp']))

            if order_local:
                for k, v in order_remote.items():
                    setattr(order_local, k, v)
            else:
                # https://stackoverflow.com/questions/31750441/generalised-insert-into-sqlalchemy-using-dictionary/31756880
                order = Order(**order_remote)
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
