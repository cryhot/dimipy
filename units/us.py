#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fractions import Fraction
from unity import Unit
from unity.units import si, imperial
"""https://en.wikipedia.org/wiki/United_States_customary_units"""


# LENGTH
in_ = imperial.in_
ft_ = imperial.ft_
yd_ = imperial.yd_
mi_ = imperial.mi_
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
gr_ = imperial.gr_
dr_ = imperial.dr_
oz_ = imperial.oz_
lb_ = imperial.lb_
cwt_ = lb_*100  # (short) hundredweight
t_   = cwt_*20  # (short) ton


del Fraction
del Unit
del si, imperial
