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
