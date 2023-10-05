#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unity import Unit
from unity.prefixes import metric as _
"""https://en.wikipedia.org/wiki/SI_derived_unit"""

s_    = Unit(_.unit, T=1) # second
m_    = Unit(_.unit, L=1) # meter
kg_   = Unit(_.unit, M=1) # kilogram
A_    = Unit(_.unit, I=1) # ampere
K_    = Unit(_.unit, Θ=1) # kelvin
mol_  = Unit(_.unit, N=1) # mole
cd_   = Unit(_.unit, J=1) # candela

ns_   = _.n*s_
µs_   = _.µ*s_
ms_   = _.m*s_
min_  = _.unit*s_ * 60
hour_ = s_ * 3600
day_  = hour_ * 24
year_ = Unit( 365*day_ + 5*hour_ + 48*min_ + 45*s_ ) # mean tropical year
week_  = day_*7
month_ = year_/12

Å_  = ang_ = m_ * 1e-10 # Ångström
nm_ = _.n*m_
µm_ = _.µ*m_
mm_ = _.m*m_
cm_ = _.c*m_
km_ = _.k*m_
au_ = m_ * 149597870700 # astronomical unit
ly_ = m_ * 9460730472580800 # light-year
pc_ = m_ * 3.085677581e16 # parsec

g_   = kg_/_.k
ng_  = _.n*g_
µg_  = _.µ*g_
mg_  = _.m*g_
t_   = kg_*1000 # ton


L_  = (_.d*m_)**3
mL_ = _.m*L_
cL_ = _.c*L_

rad_ = m_/m_
sr_ = rad_**2

Hz_  = s_ ** -1 # hertz
kHz_ = _.k*Hz_
MHz_ = _.M*Hz_
GHz_ = _.G*Hz_
N_   = Unit(M= 1, L= 1, T=-2) # newton
kN_  = N_ * 1e3
Pa_  = Unit(M= 1, L=-1, T=-2) # pascal
hPa_ = _.h*Pa_
kPa_ = _.k*Pa_
MPa_ = _.M*Pa_
GPa_ = _.G*Pa_
J_   = Unit(M= 1, L= 2, T=-2) # joule
kJ_  = _.k*J_
MJ_  = _.M*J_
GJ_  = _.G*J_
W_   = Unit(M= 1, L= 2, T=-3) # watt
kW_  = _.k*W_
MW_  = _.M*W_
GW_  = _.G*W_
TW_  = _.T*W_
mW_  = _.m*W_
Wh_  = W_ * hour_
kWh_ = _.k*Wh_
MWh_ = _.M*Wh_
GWh_ = _.G*Wh_
mA_  = _.m*A_
C_   = Unit(T=1, I=1) # coulomb
V_   = Unit(M=1, L=2, I=-1, T=-3) # volt
µV_  = _.µ*V_
mV_  = _.m*V_
F_   = Unit(I=2, T=4, M=-1, L=-2) # farad
Ω_   = ohm_ = Unit(M=1, L=2, I=-2, T=-3) # ohm
µΩ_  = µohm_ = _.µ*Ω_
mΩ_  = mohm_ = _.m*Ω_
kΩ_  = kohm_ = _.k*Ω_
MΩ_  = Mohm_ = _.M*Ω_
GΩ_  = Gohm_ = _.G*Ω_
S_   = Unit(M=-1, L=-2, T= 3, I= 2) # siemens
Wb_  = Unit(M= 1, L= 2, T=-2, I=-1) # weber
T_   = Unit(M= 1, T=-2, I=-1) # tesla
H_   = Unit(M= 1, L= 2, T=-2, I=-2) # henry
lm_  = cd_/sr_# lumen
lx_  = lm_/m_**2 # lux


del Unit
del _