#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
https://en.wikipedia.org/wiki/SI_derived_unit
https://en.wikipedia.org/wiki/Non-SI_units_mentioned_in_the_SI
"""
from fractions import Fraction
from ..core import Unit
from ..prefixes import metric as _
from .. import dimensions as dim

s_    = Unit(_.unit, dim.time) # second
m_    = Unit(_.unit, dim.length) # meter
kg_   = Unit(_.unit, dim.mass) # kilogram
A_    = Unit(_.unit, dim.electric.current) # ampere
K_    = Unit(_.unit, dim.thermodynamic_temperature) # kelvin
mol_  = Unit(_.unit, dim.amount_of_substance) # mole
cd_   = Unit(_.unit, dim.luminous.intensity) # candela

ns_   = _.n*s_
µs_   = _.µ*s_
ms_   = _.m*s_
min_  = s_ * 60
h_ = min_ * 60
d_ = h_ * 24
y_ = yr_ = Unit( 365*d_ + 5*h_ + 48*min_ + 45*s_ ) # mean tropical year (this is not SI)
week_  = d_*7
month_ = y_/12

Å_  = ang_ = m_ * 1e-10 # Ångström
nm_ = _.n*m_
µm_ = _.µ*m_
mm_ = _.m*m_
cm_ = _.c*m_
km_ = _.k*m_

g_   = kg_/_.k
ng_  = _.n*g_
µg_  = _.µ*g_
mg_  = _.m*g_
t_   = kg_*1000 # ton

ha_ = (_.h*m_)**2 # hectare

L_  = (_.d*m_)**3 # litre
mL_ = _.m*L_
cL_ = _.c*L_
dL_ = _.d*L_

rad_ = Unit(m_/m_, dim.angle) # radian
sr_ = dim.solid_angle+ rad_**2 # steradian

Hz_  = s_**-1 # hertz
kHz_ = _.k*Hz_
MHz_ = _.M*Hz_
GHz_ = _.G*Hz_
THz_ = _.T*Hz_
N_   = dim.force+ kg_*m_/s_**2 # newton
kN_  = N_ * 1e3
Pa_  = dim.pressure+ N_/m_**2 # pascal
hPa_ = _.h*Pa_
kPa_ = _.k*Pa_
MPa_ = _.M*Pa_
GPa_ = _.G*Pa_
J_   = dim.energy+ N_*m_ # joule
kJ_  = _.k*J_
MJ_  = _.M*J_
GJ_  = _.G*J_
W_   = dim.power+ J_/s_ # watt
kW_  = _.k*W_
MW_  = _.M*W_
GW_  = _.G*W_
TW_  = _.T*W_
mW_  = _.m*W_
Wh_  = dim.energy+ W_*h_
kWh_ = _.k*Wh_
MWh_ = _.M*Wh_
GWh_ = _.G*Wh_
mA_  = _.m*A_
C_   = dim.electric.charge+ A_*s_ # coulomb
V_   = dim.electric.potential+ W_/A_ # volt
µV_  = _.µ*V_
mV_  = _.m*V_
F_   = dim.electric.capacitance+ C_/V_ # farad
S_   = dim.electric.conductance+ F_/s_ # siemens
Ω_   = ohm_ = dim.electric.resistance+ S_**-1 # ohm
µΩ_  = µohm_ = _.µ*Ω_
mΩ_  = mohm_ = _.m*Ω_
kΩ_  = kohm_ = _.k*Ω_
MΩ_  = Mohm_ = _.M*Ω_
GΩ_  = Gohm_ = _.G*Ω_
Wb_  = dim.magnetic.flux+ V_*s_ # weber
T_   = dim.magnetic.induction+ Wb_/m_**2 # tesla
H_   = dim.electric.inductance+ Wb_/A_ # henry
lm_  = dim.luminous.flux+ cd_*sr_ # lumen
lx_  = dim.luminous.illuminance+ lm_/m_**2 # lux

from .angle import (deg_,arcmin_,arcsec_)
from ..constants import defined as cst
eV_ = V_*cst.e # electronvolt


del Fraction
del Unit
del _
del cst, dim