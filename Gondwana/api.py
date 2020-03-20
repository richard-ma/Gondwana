#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from Gondwana.model import db, Channel

bp = Blueprint('api', __name__, url_prefix='/api')


# /api/order/json/<str:id>
@bp.route('/order/json/<string:id>', methods=('GET',))
def api_order_json(id: str):
    return 'api_order_json';
