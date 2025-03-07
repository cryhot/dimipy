#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..core import Unit
from fractions import Fraction
from .. import params
unit = params.get('_unitary_scale', Fraction(1))
assert unit == 1, f"params['_unitary_scale'] must be unitary, got {unit!r}"
unit = Unit.SCALAR * unit
del Unit, Fraction, params

from .metric import *
__all__ = [
    k
    for k,v in globals().items()
    if v.__class__.__name__ != 'module'  # don't import submodules with *
]