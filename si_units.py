#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unity import Unit
"""https://en.wikipedia.org/wiki/SI_derived_unit"""

s_    = Unit(T=1) # second
m_    = Unit(L=1) # meter
kg_   = Unit(M=1) # kilogram
A_    = Unit(I=1) # ampere
K_    = Unit(Θ=1) # kelvin
mol_  = Unit(N=1) # mole
cd_   = Unit(J=1) # candela

ns_   = s_ * 1e-9
µs_   = s_ * 1e-6
ms_   = s_ * 1e-3
min_  = s_ * 60
hour_ = s_ * 3600
day_  = hour_ * 24
year_ = Unit( 365*day_ + 5*hour_ + 48*min_ + 45*s_ ) # mean tropical year

Å_  = ang_ = m_ * 1e-10 # Ångström
nm_ = m_ * 1e-9
µm_ = m_ * 1e-6
mm_ = m_ * 1e-3
km_ = m_ * 1e3
au_ = m_ * 149597870700 # astronomical unit
ly_ = m_ * 9460730472580800 # light-year
pc_ = m_ * 3.085677581e16 # parsec

g_   = kg_ * 1e-3
ng_  = g_ * 1e-9
µg_  = g_ * 1e-6
mg_  = g_ * 1e-3


Hz_  = s_ ** -1 # hertz
kHz_ = Hz_ * 1e3
MHz_ = Hz_ * 1e6
GHz_ = Hz_ * 1e9
N_   = Unit(M= 1, L= 1, T=-2) # newton
Pa_  = Unit(M= 1, L=-1, T=-2) # pascal
hPa_  = Pa_ * 1e2
kPa_  = Pa_ * 1e3
MPa_  = Pa_ * 1e6
GPa_  = Pa_ * 1e9
J_   = Unit(M= 1, L= 2, T=-2) # joule
kJ_  = J_ * 1e3
MJ_  = J_ * 1e6
GJ_  = J_ * 1e9
W_   = Unit(M= 1, L= 2, T=-3) # watt
kW_  = W_ * 1e3
MW_  = W_ * 1e6
GW_  = W_ * 1e9
Wh_  = W_ * hour_
kWh_ = Wh_ * 1e3
MWh_ = Wh_ * 1e6
GWh_ = Wh_ * 1e9
C_   = Unit(T= 1, I=1) # coulomb
V_   = Unit(M= 1, L= 2, T=-3, I=-1) # volt
µV_  = V_ * 1e-6
mV_  = V_ * 1e-3
F_   = Unit(M=-1, L=-2, T= 4, I= 2) # farad
Ω_   = ohm_ = Unit(M= 1, L= 2, T=-3, I=-2) # ohm
mΩ_  = mohm_ = Ω_ * 1e-3
kΩ_  = kohm_ = Ω_ * 1e3
MΩ_  = Mohm_ = Ω_ * 1e6
GΩ_  = Gohm_ = Ω_ * 1e9
S_   = Unit(M=-1, L=-2, T= 3, I= 2) # siemens
Wb_  = Unit(M= 1, L= 2, T=-2, I=-1) # weber
T_   = Unit(M= 1, T=-2, I=-1) # tesla
H_   = Unit(M= 1, L= 2, T=-2, I=-2) # henry

del Unit
