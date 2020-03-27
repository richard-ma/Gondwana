#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from Gondwana.model import *
from Gondwana.helper import *

bp = Blueprint('api', __name__, url_prefix='/api')


# /api/order/json/<str:id>
# https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
@bp.route('/order/json/<string:id>', methods=('GET',))
def api_order_json(id: str):
    order = Order.query.filter(Order.id==id).first()
    return order.as_dict()

# /api/order/update/attr/<str:id>
# https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
@bp.route('/order/update/attr/<string:id>', methods=('POST',))
def api_order_update(id: str):
    key = request.form.get('key')
    value = request.form.get('value')

    order = Order.query.filter(Order.id==id).first()

    if key in get_model_keys(Order):
        # https://stackoverflow.com/questions/23152337/how-to-update-sqlalchemy-orm-object-by-a-python-dict
        setattr(order, key, value)
        db.session.commit() # save to database

    return order.as_dict()
