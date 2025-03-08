#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""https://en.wikipedia.org/wiki/2019_redefinition_of_the_SI_base_units#Defining_constants"""
from fractions import Fraction
from ..units import si as _
from . import math

from .. import params
unit = params.get('_unitary_amount', Fraction(1))
assert unit == 1, f"params['_unitary_amount'] must be unitary, got {unit!r}"

Δv_Cs = unit*Fraction("9192631770") * (_.Hz_) # hyperfine structure transition frequency of the caesium-133
c = unit*Fraction("299792458") * (_.m_/_.s_) # speed of light
h = unit*Fraction("6.62607015e-34") * (_.J_*_.s_) # Plank constant
e = unit*Fraction("1.602176634e-19") * (_.C_) # elementary charge
k_B = unit*Fraction("1.380649e-23") * (_.J_/_.K_) # Boltzmann constant
N_A = unit*Fraction("6.02214076e23") * (_.mol_**-1) # Avogadro constant
K_cd = unit*Fraction("683") * (_.lm_/_.W_) # luminous efficacity at 540*THz_

ħ = h / (2*math.pi) # reduced Planck constant
R = N_A*k_B # gas constant
zero_celsius = unit*Fraction("273.15") * (_.K_) # 0°C

g_0 = unit*Fraction("9.80665") * (_.m_/_.s_**2) # standard Earth gravity


del Fraction
del _
del math
del params,unit