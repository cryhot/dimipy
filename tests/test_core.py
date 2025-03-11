#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pytest

from utils import *
from test_imports import src

@pytest.fixture(scope='session')
def Dimension(src):
    with dep.suppress(): return src.Dimension
@pytest.fixture(scope='session')
def Unit(src):
    with dep.suppress(): return src.Unit
@pytest.fixture(scope='session')
def Quantity(src):
    with dep.suppress(): return src.Quantity

from fractions import Fraction
Numerics = [int,float,Fraction]
zero = [
    0,
    0.,
    Fraction(0),
]
unitary = [
    1,
    1.,
    Fraction(1),
]
nonzero = [
    *unitary[:1],
    2,
    Fraction(1,2),
    3.14,
]
numeric = [
    *nonzero,
    *zero[:1],
    # 0.,
    float('inf'),
    # float('nan'),
]
dimensions = [
    dict(),
    dict(A=1),
    dict(A=-1),
    dict(A=1,B=1),
]

"""Naming convention
names for Dimension, Unit, Quantity, Numeric test objects:
    d1, u12, q123, a003 (here, dim=1, scale=2, amount=3, 0 for unspecified)
for a matrix of parametters, where if the prefix(eg 1, or 12) match, they are correlated
eg: u11_, q121 have the same dim but not the same unit
eg: u01_, q012, a003 are all dimentionless but with distinct unit
"""

@pytest.fixture(scope='module')
def d0(Dimension, request): return Dimension()
@pytest.fixture(params=dimensions, scope='module')
def d1(Dimension, request): return Dimension(request.param)
@pytest.fixture(params=dimensions, scope='module')
def d2(Dimension, request): return Dimension(request.param)

@pytest.fixture(params=[None,*unitary], scope='module')
def u00_(Unit,request,d0):
    kwargs = dict(scale=request.param,dim=d0)
    if request.param is None: kwargs.pop('scale')
    return Unit(**kwargs)
@pytest.fixture(params=nonzero, scope='module')
def u01_(Unit,request,d0): return Unit(scale=request.param,dim=d0)
@pytest.fixture(params=nonzero, scope='module')
def u11_(Unit,request,d1): return Unit(scale=request.param,dim=d1)
@pytest.fixture(params=nonzero, scope='module')
def u12_(Unit,request,d1): return Unit(scale=request.param,dim=d1)
@pytest.fixture(params=nonzero, scope='module')
def u21_(Unit,request,d2): return Unit(scale=request.param,dim=d2)

@pytest.fixture(params=[None,*zero], scope='module')
def q000(Quantity,request,u00_):
    kwargs = dict(amount=request.param,unit=u00_)
    if request.param is None: kwargs.pop('amount')
    return Quantity(**kwargs)
@pytest.fixture(params=numeric, scope='module')
def q001(Quantity,request,u00_): return Quantity(amount=request.param,unit=u00_)
@pytest.fixture(params=numeric, scope='module')
def q011(Quantity,request,u01_): return Quantity(amount=request.param,unit=u01_)
@pytest.fixture(params=numeric, scope='module')
def q111(Quantity,request,u11_): return Quantity(amount=request.param,unit=u11_)
@pytest.fixture(params=numeric, scope='module')
def q121(Quantity,request,u12_): return Quantity(amount=request.param,unit=u12_)
@pytest.fixture(params=numeric, scope='module')
def q211(Quantity,request,u21_): return Quantity(amount=request.param,unit=u21_)

@pytest.fixture(params=zero, scope='module')
def a000(request): return request.param
@pytest.fixture(params=numeric, scope='module')
def a001(request): return request.param
@pytest.fixture(params=numeric, scope='module')
def a002(request): return request.param

def test_new_dimension(Dimension):
    d = Dimension(A=1,B=2,**{'$':3})
    with pytest.raises(TypeError): d['A'] = 1
    with pytest.raises(TypeError): d.pop()
    assert Dimension(A=1)['A'] == 1
    assert Dimension(A=1)['B'] == 0
    assert Dimension(A=1)
    assert not Dimension()

def test_new_unit(Unit, d1):
    u_ = Unit(2,d1,A=1,B=2,**{'$':3})
    with pytest.raises(TypeError): u_.dim *= 2
    assert Unit(3,d1).scale == 3
    assert Unit(3,d1).dim == d1
    assert Unit(3,**d1).dim == d1

def test_new_quantity(Quantity, u11_):
    q = Quantity(2,u11_)
    q.amount *= 2
    assert Quantity(3,u11_).amount == 3
    assert Quantity(3,u11_).unit == u11_

def test_dimof_d(src,d1):   assert src.Dimension.dim_of(d1)   is d1
def test_dimof_u(src,u11_): assert src.Dimension.dim_of(u11_) is u11_.dim
def test_dimof_q(src,q111): assert src.Dimension.dim_of(q111) is q111.unit.dim
def test_dimof_a(src,a001): assert src.Dimension.dim_of(a001) is src.Dimension.NODIM

def test_d_mul_d(src,d1  ,d2  ): assert isinstance(d1  *d2  , src.Dimension)
def test_u_mul_u(src,u11_,u21_): assert isinstance(u11_*u21_, src.Unit)
def test_u_mul_q(src,u11_,q211): assert isinstance(u11_*q211, src.Unit)
def test_q_mul_u(src,q111,u21_): assert isinstance(q111*u21_, (src.Quantity,*Numerics))
def test_q_mul_q(src,q111,q211): assert isinstance(q111*q211, (src.Quantity,*Numerics))

def test_u_add_u(src,u11_,u12_): assert u11_+ u12_ is u12_
def test_u_add_d(src,u11_,d1  ): assert u11_ +d1 is u11_
def test_d_add_u(src,d1  ,u12_): assert d1+ u12_ is u12_
def test_d_add_d(src,d1       ): assert src.Dimension(d1)+ d1 is d1
def test_q_add_u(src,q111,u12_): assert src.Quantity(q111 +u12_).unit == u12_
def test_u_add_q(src,u11_,q121): assert src.Quantity(u11_+ q121).unit == src.Quantity(q121).unit
def test_q_add_q(src,q111,q121): assert src.Quantity(q111 + q121).unit == src.Quantity(q121).unit
def test_q_add_d(src,q111,d1  ): assert q111 +d1 is q111
def test_d_add_q(src,d1  ,q121): assert d1+ q121 is q121

if __name__ == "__main__":
    # invokes `python3 -m pytest`
    sys.exit(pytest.main([
        __file__,
        # '-rNf', # Get rid of (E)rrors
        # '-rP',  # Show passed tests outputs
        # '-s',   # Show Output, do not capture
        *sys.argv[1:],
    ]))