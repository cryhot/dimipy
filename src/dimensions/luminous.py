#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""https://en.wikipedia.org/wiki/Photometry_(optics)#Photometric_quantities"""

from fractions import Fraction
from ..core import Dimension
from .. import dimensions as dim

# BASE DIMENSIONS
intensity = Dimension(J=1)

# DERIVED DIMENSIONS
flux = intensity*dim.solid_angle
energy = flux*dim.time
luminance = intensity/dim.surface
illuminance = flux/dim.surface
excitance = flux/dim.surface
exposure = illuminance*dim.time

# ALIASES
luminosity = intensity
power = flux
emmitance = excitance

del Fraction
del Dimension
del dim