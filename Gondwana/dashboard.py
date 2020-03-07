#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash

bp = Blueprint('dashboard', __name__)

# /
@bp.route('/', methods=('GET',))
def index():
    return render_template('dashboard/index.html')
