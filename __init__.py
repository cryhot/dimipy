#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .core import Dimension, Unit, Quantity

def dim_of(obj):
    return Dimension.dim_of(obj)

def isdimension(obj, dimension):
    if isinstance(dimension, tuple):
        return any(isdimension(obj, d) for d in dimension)
    return dim_of(obj) == dim_of(dimension)

def assertDimension(obj, dimension):
    assert isdimension(obj, dimension), "wrong dimension: [{}] expected, got [{}]".format(
        dim_of(obj), dim_of(dimension),
    )
