#!/usr/bin/env python
# encoding: utf-8

import click, json
from datetime import datetime
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import event
from pycscart import Cscart

db = SQLAlchemy()
migrate = Migrate()


# models
class BaseModel(object):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Channel(BaseModel, db.Model):
    __tablename__ = 'channel'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)  # Channel名称
    website_url = db.Column(db.String(128), unique=True)  # Cscart网站的URL
    email = db.Column(db.String(128), nullable=False)  # 管理员email
    api_key = db.Column(db.String(128), nullable=False)  # API KEY

    orders = db.relationship('Order',
            backref=db.backref('channel'),
            cascade='all, delete-orphan') # cascade delete: https://graycarl.me/2014/03/24/sqlalchemy-cascade-delete.html


class Order(BaseModel, db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer)  # 订单ID
    status = db.Column(db.String(1))  # 订单状态

    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))

    # customer information
    firstname = db.Column(db.String(32))  # 订单名
    lastname = db.Column(db.String(32))  # 订单姓
    phone = db.Column(db.String(32))  # 电话
    fax = db.Column(db.String(32))  # 传真
    url = db.Column(db.String(32))  # 网址
    email = db.Column(db.String(128))  # email
    ip_address = db.Column(db.String(32))  # IP地址

    # bill information
    b_firstname = db.Column(db.String(32))  # 账单名
    b_lastname = db.Column(db.String(32))  # 账单姓
    b_address = db.Column(db.String(255))  # 账单地址
    b_address_2 = db.Column(db.String(255))  # 账单地址2
    b_city = db.Column(db.String(64))  # 账单城市
    b_county = db.Column(db.String(32))  #
    b_state = db.Column(db.String(32))  # 账单州
    b_country = db.Column(db.String(2))  # 账单国家
    b_zipcode = db.Column(db.String(32))  # 账单邮编
    b_phone = db.Column(db.String(32))  # 账单电话
    b_country_descr = db.Column(db.String(128))  # 账单国家全称
    b_state_descr = db.Column(db.String(255))  # 账单州全称

    # shipping information
    s_firstname = db.Column(db.String(32))  # 运单名
    s_lastname = db.Column(db.String(32))  # 运单姓
    s_address = db.Column(db.String(255))  # 运单地址
    s_address_2 = db.Column(db.String(255))  # 运单地址2
    s_city = db.Column(db.String(64))  # 运单城市
    s_county = db.Column(db.String(32))  #
    s_state = db.Column(db.String(32))  # 运单州
    s_country = db.Column(db.String(2))  # 运单国家
    s_zipcode = db.Column(db.String(32))  # 运单邮编
    s_phone = db.Column(db.String(32))  # 运单电话
    s_address_type = db.Column(db.String(32))  # 运单地址类型
    s_country_descr = db.Column(db.String(128))  # 运单国家全称
    s_state_descr = db.Column(db.String(255))  # 运单州全称

    # products
    products = db.Column(db.Text) # 产品信息
    total = db.Column(db.Float)  # 订单合计

    # others
    shipping_method = db.Column(db.String(255)) # 快递方式
    timestamp = db.Column(db.DateTime) # 下单时间

# event listener

# event helper
def convert_before_save(target):
    # https://www.geeksforgeeks.org/python-convert-dictionary-object-into-string/
    target.products = json.dumps(target.products)
    # https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date
    target.timestamp = datetime.utcfromtimestamp(int(target.timestamp))
    return target

# synchronize order.status to channel
# https://docs.sqlalchemy.org/en/13/orm/events.html?highlight=after_update#sqlalchemy.orm.events.MapperEvents.after_update
@event.listens_for(Order, 'before_update')
def order_before_update(mapper, connection, target):
    api = Cscart(target.channel.website_url, target.channel.email, target.channel.api_key)
    api.update_order_status(str(target.order_id), target.status)
    target = convert_before_save(target)

# products: convert python dictionary to string
@event.listens_for(Order, 'before_insert')
def order_before_insert(mapper, connection, target):
    target = convert_before_save(target)

# products: convert string to python dictionary
@event.listens_for(Order, 'load')
def order_load(instance, context):
    instance.products = json.loads(instance.products)

'''
    subtotal = db.Column(db.Float)  #
    discount = db.Column(db.Float)  # 折扣
    subtotal_discount = db.Column(db.Float)  #
    payment_surcharge = db.Column(db.Float)  #
    shipping_ids = db.Column(db.String(32)) # 物流ID
    shipping_cost = db.Column(db.Float) # 运费
    notes = db.Column(db.Text) # 订单备注
    details = db.Column(db.Text) #
    company = db.Column(db.String(32)) #
    need_shipping = db.Column(db.Boolean) # 是否需要运送

    tax_exempt = db.Column(db.String(32))
    lang_code = db.Column(db.String(8)) # 语言代码
    re_paid = db.Column(db.String(32))
    validation_code = db.Column(db.String(32))
    secondary_currency = db.Column(db.String(32)) # 次要货币
    display_subtotal = db.Column(db.Float)
'''
