#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from Gondwana.model import db, Order

bp = Blueprint('api', __name__, url_prefix='/api')


# /api/order/json/<str:id>
# https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
@bp.route('/order/json/<string:id>', methods=('GET',))
def api_order_json(id: str):
    order = Order.query.filter(Order.id==id).first()
    return order.as_dict()
