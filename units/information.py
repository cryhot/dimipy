#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""https://en.wikipedia.org/wiki/Units_of_information"""

from unity import prefixes as _
from unity import Unit
b_ = bit_ = Unit(_.unit, Bit=1)
B_ = byte_ = b_ * 8
del Unit

from unity.prefixes import metric as _
kb_ = kB_ = _.k*b_
Mb_ = _.M*b_
Gb_ = _.G*b_
Tb_ = _.T*b_
Pb_ = _.P*b_

kB_ = KB_ = _.k*B_
MB_ = _.M*B_
GB_ = _.G*B_
TB_ = _.T*B_
PB_ = _.P*B_

from unity.prefixes import binary as _
Kib_ = _.Ki*b_
Mib_ = _.Mi*b_
Gib_ = _.Gi*b_
Tib_ = _.Ti*b_
Pib_ = _.Pi*b_

KiB_ = _.Ki*B_
MiB_ = _.Mi*B_
GiB_ = _.Gi*B_
TiB_ = _.Ti*B_
PiB_ = _.Pi*B_

del _