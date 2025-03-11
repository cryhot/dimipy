#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fractions import Fraction
from ..units import si as _

from .math import *
from .defined import *
del Δv_Cs # who cares?                                              # noqa: F821

# m_u = ...
G = 6.6743015e-11 * (_.N_*_.m_**2*_.kg_**-2) # Gravitational constant
k_e = 8.987551792314e9 * (_.N_*_.m_**2*_.C_**-2) # Coulomb constant
ϵ_0 = 1/(4*π * k_e) # vacuum electric permitivity
µ_0 = 1/(ϵ_0 * c**2) # vacuum magnetic permeability
α = e**2 / (2 * ϵ_0 * h * c) # fine-structure constant
m_e = 9.109383701528e-31 * (_.kg_) # electron mass

del Fraction
del _
__all__ = [
    k
    for k,v in globals().items()
    if not k.startswith("_")
    if v.__class__.__name__ != 'module'  # don't import submodules with *
]