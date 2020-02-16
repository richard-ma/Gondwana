#!/usr/bin/env python
# encoding: utf-8

import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


# models
class Channel(db.Model):
    __tablename__ = 'channel'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)  # Channel名称
    website_url = db.Column(db.String(128), unique=True)  # Cscart网站的URL
    email = db.Column(db.String(128), nullable=False)  # 管理员email
    api_key = db.Column(db.String(128), nullable=False)  # API KEY

    def __init__(self, name, website_url, email, api_key):
        self.name = name
        self.website_url = website_url
        self.email = email
        self.api_key = api_key


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.String(32))  # 订单ID
    is_parent_order = db.Column(db.String(1))  # 是否是父订单
    total = db.Column(db.String(32))  # 订单合计
    subtotal = db.Column(db.String(32))  #
    discount = db.Column(db.String(32))  # 折扣
    subtotal_discount = db.Column(db.String(32))  #
    payment_surcharge = db.Column(db.String(32))  #
    shipping_ids = db.Column(db.String(32)) # 物流ID
    shipping_cost = db.Column(db.String(32)) # 运费
    timestamp = db.Column() # 时间戳
    status = db.Column(db.String(32)) # 订单状态
    notes = db.Column(db.String(128)) # 订单备注
    details = db.Column(db.String(32)) #
    firstname = db.Column(db.String(32)) # 订单名
    lastname = db.Column(db.String(32)) # 订单姓
    company = db.Column(db.String(32)) #

    b_firstname = db.Column(db.String(32)) # 账单名
    b_lastname = db.Column(db.String(32)) # 账单姓
    b_address = db.Column(db.String(128)) # 账单地址
    b_address_2 = db.Column(db.String(128)) # 账单地址2
    b_city = db.Column(db.String(64)) # 账单城市
    b_county = db.Column(db.String(32)) #
    b_state = db.Column(db.String(32)) # 账单州
    b_country = db.Column(db.String(32)) # 账单国家
    b_zipcode = db.Column(db.String(16)) # 账单邮编
    b_phone = db.Column(db.String(16)) # 账单电话
    b_country_descr = db.Column(db.String(128)) # 账单国家全称
    b_state_descr = db.Column(db.String(128)) # 账单州全称

    s_firstname = db.Column(db.String(32)) # 运单名
    s_lastname = db.Column(db.String(32)) # 运单姓
    s_address = db.Column(db.String(128)) # 运单地址
    s_address_2 = db.Column(db.String(128)) # 运单地址2
    s_city = db.Column(db.String(64)) # 运单城市
    s_county = db.Column(db.String(32)) #
    s_state = db.Column(db.String(32)) # 运单州
    s_country = db.Column(db.String(32)) # 运单国家
    s_zipcode = db.Column(db.String(16)) # 运单邮编
    s_phone = db.Column(db.String(16)) # 运单电话
    s_address_type = db.Column(db.String(32)) # 运单地址类型
    s_country_descr = db.Column(db.String(128)) # 运单国家全称
    s_state_descr = db.Column(db.String(128)) # 运单州全称
    need_shipping = db.Column(db.Boolean()) # 是否需要运送

    phone = db.Column(db.String(16)) # 电话
    fax = db.Column(db.String(16)) # 传真
    url = db.Column(db.String(128)) # 网址
    email = db.Column(db.String(128)) # email
    tax_exempt = db.Column(db.String(32))
    lang_code = db.Column(db.String(8)) # 语言代码
    ip_address = db.Column(db.String(32)) # IP地址
    re_paid = db.Column(db.String(32))
    validation_code = db.Column(db.String(32))
    secondary_currency = db.Column(db.String(32)) # 次要货币
    display_subtotal = db.Column(db.String(32))


# command line
@click.command('init-db')
@with_appcontext
def init_db_command():
    db.create_all()
    click.echo('Initialized the database.')
