#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""https://en.wikipedia.org/wiki/United_States_customary_units"""
from fractions import Fraction
from ..core import Unit
from . import si, imperial

# TIME
from .si import (s_,min_,h_,d_,)


# LENGTH
from .imperial import (in_, ft_, yd_, mi_,)
P_  = in_/6 # pica
p_  = P_/12 # point

# VOLUME
gal_ = in_**3 * 231 # gallon
pot_   = gal_/2     # pottle
qt_    = gal_/4     # quart
pt_    = gal_/8     # pint
c_=cup_= pt_/2      # cup
gi_    = pt_/4      # gill
fl_oz_ = pt_/16     # fluid ounce
tbsp_  = fl_oz_/2   # tablespoon
tsp_   = tbsp_/3    # teaspoon
jig_   = tbsp_*3    # shot
fl_dr_ = tbsp_/4    # fluid dram
min_   = fl_dr_/60  # minim

# MASS
from .imperial import (gr_, dr_, oz_, lb_,)
cwt_ = lb_*100  # (short) hundredweight
t_   = cwt_*20  # (short) ton

# DERIVED UNITS
from .imperial import (mph_,lbf_, psi_,)


del Fraction
del Unit
del si, imperial
