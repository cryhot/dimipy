#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""https://en.wikipedia.org/wiki/Units_of_information"""
from .si import (s_,)

from .. import prefixes as _
from ..core import Unit
b_ = bit_ = Unit(_.unit, Bit=1)
B_ = byte_ = b_ * 8
del Unit

from ..prefixes import metric as _
kb_ = Kb_ = _.k*b_
Mb_ = _.M*b_
Gb_ = _.G*b_
Tb_ = _.T*b_
Pb_ = _.P*b_

kB_ = KB_ = _.k*B_
MB_ = _.M*B_
GB_ = _.G*B_
TB_ = _.T*B_
PB_ = _.P*B_

kbps_ = Kbps_ = kb_/s_
Mbps_ = Mb_/s_
Gbps_ = Gb_/s_
Tbps_ = Tb_/s_
Pbps_ = Pb_/s_

kBps_ = KBps_ = kB_/s_
MBps_ = MB_/s_
GBps_ = GB_/s_
TBps_ = TB_/s_
PBps_ = PB_/s_

from ..prefixes import binary as _
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

Kibps_ = Kib_/s_
Mibps_ = Mib_/s_
Gibps_ = Gib_/s_
Tibps_ = Tib_/s_
Pibps_ = Pib_/s_

KiBps_ = KiB_/s_
MiBps_ = MiB_/s_
GiBps_ = GiB_/s_
TiBps_ = TiB_/s_
PiBps_ = PiB_/s_

del _
del (s_,)