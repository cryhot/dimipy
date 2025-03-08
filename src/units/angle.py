#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""https://en.wikipedia.org/wiki/Angle#Units"""
from ..prefixes import metric as _
from ..constants.math import pi

from .si import (rad_, sr_,)
turn_ = rad_*2*pi
deg_ = turn_/360
arcmin_ = deg_/60
arcsec_ = arcmin_/60

del pi
del _