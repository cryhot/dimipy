#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fractions import Fraction
from unity import Unit
from unity.units import si
"""https://en.wikipedia.org/wiki/Imperial_units"""

# LENGTH
yd_ = si.m_ * Fraction("0.9144") # yard
ft_  = yd_/3    # feet
hh_  = ft_/3    # hand
in_  = hh_/4    # inch
ch_  = yd_*22   # chain
fur_ = ch_*10   # furlong
mi_  = fur_*8   # mile
lea_ = mi_*3    # league
nmi_   = si.m_ * Fraction("1852") # nautical mile
cable_ = nmi_/10    # cable
ftm_   = nmi_/1000  # fathom

# VOLUME
gal_ = si.L_ * Fraction("4.54609") # gallon
qt_    = gal_/4 # quart
pt_    = gal_/8 # pint
gi_    = pt_/4  # gill
fl_oz_ = pt_/20 # fluid ounce

# MASS (avoirdupois)
lb_ = si.kg_ * Fraction("0.4535923") # pound
oz_  = lb_/16   # ounce
dr_  = oz_/16   # dram, drachm
gr_  = lb_/7000 # grain
st_  = lb_*14   # stone
qr_  = qtr_ = st_*2 # quarter
cwt_ = st_*8    # (long) hundredweight
t_   = cwt_*20  # (long) ton

del Fraction
del Unit
del si