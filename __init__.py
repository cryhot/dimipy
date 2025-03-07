#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fractions import Fraction
# keys starting with "_" only have an effect at load time
params = dict(
    # CORE
    unwrap_scalar=True,  # return quantity when unit is Unit.SCALAR
    # UNITS
    _unitary_scale=Fraction(1),  # for unity.units.*
    _dim_angle=dict(A=1),  # use dict() for dimensionless unit
    _dim_amount_of_substance=dict(N=1),  # use dict() for dimensionless unit
    # CONSTANTS
    _unitary_amount=Fraction(1),  # for unity.constants.defined.*
)
del Fraction



from .core import Dimension, Unit, Quantity

def dim_of(obj):
    return Dimension.dim_of(obj)

def isdimension(obj, dimension):
    if isinstance(dimension, tuple):
        return any(isdimension(obj, d) for d in dimension)
    return dim_of(obj) == dim_of(dimension)

def assertDimension(obj, dimension):
    assert isdimension(obj, dimension), "wrong dimension: [{}] expected, got [{}]".format(
        dim_of(dimension), dim_of(obj),
    )



__all__ = [
    k
    for k,v in globals().items()
    if v.__class__.__name__ != 'module'  # don't import submodules with *
]