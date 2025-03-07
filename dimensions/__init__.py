#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""https://en.wikipedia.org/wiki/International_System_of_Quantities"""

from fractions import Fraction
from ..core import Dimension
from .. import params

dimensionless = Dimension.NODIM

# BASE DIMENSIONS
time                      = Dimension(T=1)
length                    = Dimension(L=1)
mass                      = Dimension(M=1)
electric_current          = Dimension(I=1)
thermodynamic_temperature = Dimension(Θ=1)
amount_of_substance       = Dimension(params.get('dim_amount_of_substance',dict(N=1)))
angle                     = Dimension(params.get('dim_angle',dict(A=1)))

# DERIVED DIMENSIONS
solid_angle = angle**2
frequency = time**-1
surface = length**2
volume = length**3
velocity = length/time
acceleration = velocity/time
force = mass*acceleration
pressure = force/surface
energy = force*length
power = energy/time
intensity = power/surface
density = mass/volume

from . import electric, magnetic, luminous

# ALIASES
temperature = thermodynamic_temperature
chemical_amount = amount_of_substance
speed = velocity
work = energy
heat = energy


del Fraction
del Dimension
del params
__all__ = [
    k
    for k,v in globals().items()
    if v.__class__.__name__ != 'module'  # don't import submodules with *
]