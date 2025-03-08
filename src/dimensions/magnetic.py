#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

from fractions import Fraction
from ..core import Dimension
from .. import dimensions as dim

# DERIVED DIMENSIONS
flux = dim.electric.potential*dim.time
induction = flux/dim.surface

# ALIASES
flux_density = induction

del Fraction
del Dimension
del dim