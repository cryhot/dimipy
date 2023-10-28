#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""https://en.wikipedia.org/wiki/Astronomical_system_of_units"""
from fractions import Fraction
from ..prefixes import metric as _
from . import si, angle
from ..constants import defined as cst

# TIME
from .si import (s_,min_,h_,d_,)
y_ = yr_  = d_ * Fraction("365.25") # julian year

# LENGTH
from .si import (m_,km_,)
Gm_ = _.G*m_
au_ = m_ * 149597870700 # astronomical unit
ly_ = y_ * cst.c # light-year
pc_ = au_/(angle.arcsec_/angle.rad_) # parsec
kpc_ = _.k*pc_
Mpc_ = _.M*pc_
Gpc_ = _.G*pc_
LD_ = Δ_EL_ = 3.84399e8 * m_ # Δ_⊕L, Lunar distance, ≈

# MASS
M_E_ = M_earth_ = 1.988e30 * si.kg_ # M_☉, solar mass, ≈
M_J_ = M_jupiter_ = 1.89813e27 * si.kg_ # M_♃, Jupiter mass, ≈
M_S_ = M_sun_ = 5.9722e24 * si.kg_ # M_⊕, Earth mass, ≈

del Fraction
del _
del si, angle
del cst