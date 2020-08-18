#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from Gondwana.model import db, Setting

bp = Blueprint('settings', __name__, url_prefix='/settings')


# /settings/index
@bp.route('/index', methods=('GET',))
def settings_index():
    settings = Setting.query.all()

    return render_template('settings/index.html', active_page="settings_index", settings=settings)
