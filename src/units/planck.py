#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""https://en.wikipedia.org/wiki/Planck_units"""
from fractions import Fraction
from ..core import Unit
from ..prefixes import metric as _
from . import si, angle
from .. import constants as cst
from .. import dimensions as dim

v_p_ = Unit(cst.c) +dim.velocity
l_P_ = Unit(( cst.ħ * cst.G * cst.c**-3 )**.5) +dim.length
m_P_ = Unit(( cst.ħ * cst.c * cst.G**-1 )**.5) +dim.mass
t_P_ = Unit(( cst.ħ * cst.G * cst.c**-5 )**.5) +dim.time
T_P_ = Unit(( cst.ħ * cst.c**5 * cst.G**-1 * cst.k_B**-2 )**.5) +dim.temperature
q_p_ = Unit(( cst.k_e**-1 * cst.ħ * cst.c )**.5) +dim.electric.charge  # for k_e=1
# q_p_ = Unit(( cst.ϵ_0 * cst.ħ * cst.c )**.5) +dim.electric.charge  # for ϵ_0=1
E_P_ = m_P_ * v_p_**2 +dim.energy
F_P_ = E_P_ / l_P_ +dim.force
ρ_P_ = m_P_ / l_P_**3 +dim.density
a_P_ = v_p_ / t_P_ +dim.acceleration

del Fraction
del Unit
del _, cst, dim
del si, angle