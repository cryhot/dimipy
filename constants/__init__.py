#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unity.units.si as _
from math import pi

π = pi

c = 299792458 * (_.m_/_.s_) # speed of light
G = 6.6740831e-11 * ( _.N_ * (_.m_/_.kg_)**2 ) # gravitational constant
h = 6.6260704081e-34 * ( _.J_ * _.s_ ) # Plank constant
ħ = h / (2*pi) #  reduced Planck constant
R = 8.314459848 * ( _.J_ / _.mol_ / _.K_ ) # gas constant = N_A*k_B
N_A = 6.02214085774e23 * ( _.mol_**-1 ) # Avogadro constant
k_B = 1.3806485279e-23 * ( _.J_ / _.K_ ) # Boltzmann constant
e = 1.602176620898e-19 * _.C_ # elementary charge
m_e = 9.1093835611e-31 * _.kg_ # electron mass

g = 9.80665 * (_.m_/_.s_**2) # standard Earth gravity
atm = 101325 * _.Pa_ # standard Earth atmosphere

zero_celcius = 273.15 * _.K_ # 0°C

del _
