#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from Gondwana.model import db, Setting

bp = Blueprint('setting', __name__, url_prefix='/setting')


# /setting/index
@bp.route('/index', methods=('GET',))
def setting_index():
    settings = Setting.query.all()

    return render_template('setting/index.html', active_page="setting_index", settings=settings)
