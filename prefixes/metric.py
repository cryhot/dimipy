#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""https://en.wikipedia.org/wiki/Metric_prefix"""

from . import unit
subbase = unit*10
base = subbase**3

da = deca   = subbase**1
h  = hecto  = subbase**2
k  = kilo   = base**1
M  = mega   = base**2
G  = giga   = base**3
T  = tera   = base**4
P  = peta   = base**5
E  = exa    = base**6
Z  = zetta  = base**7
Y  = yotta  = base**8
R  = ronna  = base**9
Q  = quetta = base**10

d  = deci   = subbase**-1
c  = centi  = subbase**-2
m  = milli  = base**-1
µ  = micro  = base**-2
n  = nano   = base**-3
p  = pico   = base**-4
f  = femto  = base**-5
a  = atto   = base**-6
z  = zepto  = base**-7
y  = yocto  = base**-8
r  = ronto  = base**-9
q  = quecto = base**-10

del subbase, base