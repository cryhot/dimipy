#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""https://en.wikipedia.org/wiki/Binary_prefix"""

from . import unit
base = unit*1024

Ki = kibi = base**1
Mi = mebi = base**2
Gi = gibi = base**3
Ti = tebi = base**4
Pi = pebi = base**5
Ei = exbi = base**6
Zi = zebi = base**7
Yi = yobi = base**8

del base