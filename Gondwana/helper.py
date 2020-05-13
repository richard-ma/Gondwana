#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_all_order_status():
    return [
            "P",
            "C",
            "O",
            "F",
            "D",
            "B",
            "I",
            "Y",
            "A",
            "E",
            "G",
            "H",
            "J",
    ]

# https://stackoverflow.com/questions/2537471/method-of-iterating-over-sqlalchemy-models-defined-columns
from sqlalchemy import inspect
from Gondwana.model import *
def get_model_keys(cls):
    keys = list()

    if issubclass(cls, db.Model):
        mapper = inspect(cls)
        for column in mapper.attrs:
            keys.append(column.key)

    return keys

# return type of product
import re
def get_product_type_name(product_name):
    regs = {
        '童装': [
            r'(^|\s)kid(s)?\'s',
            r'(^|\s)youth',
            r'(^|\s)preschool',
            r'(^|\s)newborn',
        ],
        '女装': [
            r'(^|\s)wom[ae]n\'s',
            r'(^|\s)lad(y|ies)\'s',
        ],
        '男装': [
            r'(^|\s)m[ae]n\'s',
        ],
    }

    for k, v in regs.items():
        for pattern in v:
            if re.search(pattern, product_name, re.IGNORECASE) is not None:
                return k

    return '男装'
