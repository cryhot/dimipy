#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from fractions import Fraction
from ..core import Dimension
from .. import dimensions as dim

# BASE DIMENSIONS
current = Dimension(I=1)

# DERIVED DIMENSIONS
charge = current*dim.time
potential = dim.energy/charge
capacitance = charge/potential
conductance = current/potential
resistance = potential/current
# inductance = magnetic.flux/current
inductance = resistance*dim.time

# ALIASES
intensity = current
voltage = potential
electromotive_force = potential

del Fraction
del Dimension
del dim