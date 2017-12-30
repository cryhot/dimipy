# Unity

## Description

unit library for python3

## Content

3 levels datastructure: ``Dimention`` - ``Unit`` - ``Quantity``
- `Dimention`: relates to a physical dimention (immutable)
- `Unit`: describes a physical unit (immutable)
- `Quantity`: describes a certain amount of a given unit

Basic rules for `Unit`, `Quantity` and other types operations:
- an ordinary object is considered as a `Quantity` object whose Unit is `Unit.SCALAR` (no dimention, scale `1`)
- if the result of an operation is a `Quantity` whose Unit has no dimention and scale `1`, the result is substituted with the quantity itself
- the result of **(A \* B)** has the **type of A** (so n\*`Unit` is a `Quantity` but `Unit`\*n is a new `Unit`)
- the result of **(A \+ B)** is a `Quantity` (unless A and B are `Units`) and has the **unit of B** (`Quantity` + `Unit` gives the same Quantity but converted in the given Unit)

## Examples

```py
# dimentions
length = Dimention(L=1)
speed  = Dimention(L=1, T=-1)
acceleration = Dimention(L=1, T=-2)

# unit definitions
_m    = Unit(scale=1, dim=length)       # a unit is composed of a dimention and a scale
_km   = Unit(scale=1000, dim=length)    # scale is relative to the SI-unit
_kn   = Unit(0.514444,speed)            # the knot definition
_kg   = Unit(M=1)
_s    = Unit(1,T=1)     # a unit with scale 1 (default)
_min  = Unit(60,T=1)    # a unit with scale 60
_hour = _s * 3600       # a unit with scale 3600 (_s must be on left)
_day  = _hour * 24      # a unit with scale 3600 * 24 = 86400
_km_h = _km / _hour     # equivalent to Unit(1000/3600, speed)
_N    = Unit(M=1,L=1,T=-2)
_J    = Unit(M=1,L=2,T=-2) + _N*_m # checks the compatibility of units (homogeneity)
_W    = Unit(M=1,L=2,T=-3) + _J/_s # actualy, _W takes the value of (_J/_s), the second term

# quantities
g = Quantity(amount=9.81, unit=Unit(acceleration))  # a quantity is composed of a unit and an amount
c = 299792.458 * (_m/_s)    # ((_m/_s) must be on right)

time = 2*_day + 12*_hour    # first convert 2*_day in _hour, then add
time.convert(_min)          # convert time in place in minutes
time.convert()              # convert time in SI, i.e. in _s
time2 = time + _day         # Quantity + Unit -> convert the quantity (time2 in _day)
time3 = _min + time         # Unit + Quantity -> only checks the compatibility (time3 still in _s)
time3 += _hour              # same as time3.convert(_hour)
b = (time2 == time3)        # True
b = ( 20*_min < 2000*_s )   # False
print( c + _km_h )          # print the speed of light in kilometers per hour
```

## What next ?

- named units and composed units
- include list of standard units
- non linear units (like celsius compared to Kelvin) - If I have time ans motivation

## Contact

Jean-Raphaël Gaglione   < jr dot gaglione at yahoo dot fr >
