# Unity

## Description

unit library for python3

## Content

3 levels datastructure: ``Dimension`` - ``Unit`` - ``Quantity``
- `Dimension`: relates to a physical dimension (immutable)
- `Unit`: describes a physical unit with it's scale (immutable)
- `Quantity`: describes a certain amount of a given unit

Basic rules for `Unit`, `Quantity` and other types operations:
- an ordinary object is considered as a `Quantity` object whose Unit is `Unit.SCALAR` (no dimension, scale `1`)
- if the result of an operation is a `Quantity` whose Unit has no dimension and scale `1` (i.e. equal to `Unit.SCALAR`), the result is substituted with the quantity itself
- the result of **(A \* B)** has the **type of A** (so n\*`Unit` is a `Quantity` but `Unit`\*n is a new `Unit`)
- the result of **(A \+ B)** is a `Quantity` (unless A and B are `Units`) and has the **unit of B** (`Quantity` + `Unit` gives the same Quantity but converted in the given Unit)

## Examples

Those examples are a quasi-exhaustive demonstration of the possibilities of this module. You don't need all of this to get started! For a simple usage with lightweight syntax, see the next paragraph.

```py
# dimensions
length = Dimension(L=1)
speed  = Dimension(L=1, T=-1)
acceleration = Dimension( {'L':1, 'T':-2} )

# unit definitions
m_    = Unit(scale=1, dim=length)       # a unit is composed of a dimension and a scale
km_   = Unit(scale=1000, dim=length)    # scale is relative to the SI-unit
kn_   = Unit(0.514444,speed)            # the knot definition
kg_   = Unit(M=1)
s_    = Unit(1,T=1)     # a unit with scale 1 (default)
min_  = Unit(60,T=1)    # a unit with scale 60
hour_ = s_ * 3600       # a unit with scale 3600 (s_ must be on left)
day_  = hour_ * 24      # a unit with scale 3600 * 24 = 86400
km_h_ = km_ / hour_     # equivalent to Unit(1000/3600, speed)
N_    = Unit(M=1,L=1,T=-2)
J_    = Unit(M=1,L=2,T=-2) + N_*m_ # checks the compatibility of units (homogeneity)
W_    = Unit(M=1,L=2,T=-3) + J_/s_ # actually, W_ takes the value of (J_/s_), the second term

# quantities
g = Quantity(amount=9.81, unit=Unit(acceleration))  # a quantity is composed of a unit and an amount
c = 299792458 * (m_/s_)    # ((m_/s_) must be on right)

time = 2*day_ + 12*hour_    # first convert 2*day_ in hour_, then add
time.convert(min_)          # convert time in place in minutes
time.convert()              # convert time in SI, i.e. in s_
time2 = time + day_         # Quantity + Unit -> convert the quantity (time2 in day_)
time3 = min_ + time         # Unit + Quantity -> only checks the compatibility (time3 still in s_)
time3 += hour_              # same as time3.convert(hour_)
b = (time2 == time3)        # True
b = ( 20*min_ < 2000*s_ )   # False
print( c + km_h_ )          # print the speed of light in kilometers per hour
```
### Predefined units and constants

<p align="center">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/SI_base_units.svg/256px-SI_base_units.svg.png">
</p>

The [SI base units](https://en.wikipedia.org/wiki/SI_base_unit) are based on 7 dimensions of measurement:

- **`'T'`** for time
- **`'L'`** for length
- **`'M'`** for mass
- **`'I'`** for electric current intensity
- **`'Θ'`** for thermodynamic temperature
- **`'M'`** for amount of substance
- **`'J'`** for luminous intensity

Those dimensions are used in the module `unity.si_units`. You can still define your own arbitrary dimensions on top of that, like **`'$'`** or **`'people'`**.

```py
from unity.si_units import * # see source file for exhaustive list of standard units
from unity.constants import c,G

u_age       =      13.799e9*year_              # year_ is defined as (s_*31556925)
u_radius    =m_+   c * u_age                   # checks that result is a length, unit will still be (m_*year_/s_) = (m_*31556925)
u_crit_mass =kg_+  0.5 * c**2 / G * u_radius   # checks that result is a mass
u_mass      =      1e53*kg_                    # https://en.wikipedia.org/wiki/Universe

print( u_crit_mass       ) # unit is kg_*31556925 = Unit[31556925 * M]
print( u_crit_mass  +kg_ ) # print it in standard units

print( u_mass / u_crit_mass     ) # unit is s_/year_ = Unit[3.1688765e-08 * 1]
print( u_mass / u_crit_mass  +0 ) # print it as a Unit.SCALAR
```

## What next?

- include more standard units and constants
- use fractions for Unit.scale
- named units and composed units
- non linear units (like celsius compared to Kelvin) - If I have time and motivation
- :warning: I might change the name of the library/submodules in the future

## Contact

Jean-Raphaël Gaglione   < jr dot gaglione at yahoo dot fr >

_If you are interested in that project, do not hesitate to contact me!_
