#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
import math
from fractions import Fraction

def ordering(key, standard=None):
    """Class decorator that implement ordering methods from key."""
    def decorator(cls):
        ops = ('__lt__', '__le__', '__gt__', '__ge__', '__eq__', '__ne__')
        def twoargs(opfunc):
            """Override function signature."""
            def opfunc2(self, value):
                return opfunc(self, value)
            return opfunc2
        for op in ops:
            if getattr(cls, op, None) is not getattr(object, op, None): continue
            @twoargs
            def opfunc(self, value, *, op=op):
                if standard is not None: value = standard(value)
                if not isinstance(value, cls): return NotImplemented
                k1,k2 = key(self),key(value)
                meth = getattr(k1, op, None)
                if meth is None: return NotImplemented
                return meth(k2)
            opfunc.__name__ = op
            opfunc.__qualname__ = "%s.%s" % (cls.__qualname__, op)
            setattr(cls, op, opfunc)
        del twoargs
        return cls
    return decorator

class DimensionError(TypeError):
    """Inappropriate dimension."""
    def __init__(self, *args, **kwds):
        super(DimensionError, self).__init__(*args, **kwds)
    @classmethod
    def from_dims(cls, from_, to):
        """Create and return a new DimensionError from two dimensions."""
        from_ = Dimension.dim_of(from_)
        to = Dimension.dim_of(to)
        return cls("inhomogeneous conversion from %s to %s"%(from_, to))
    # def from_units(from_, to):
    #     """Create and return a new DimensionError from two units."""
    #     return DimensionError("Inhomogeneous conversion from '%r' to '%r'"%(from_, to))

def _neatscale(value):
    """Transform a value in a neater value"""
    if isinstance(value, Fraction): return value
    try:
        if value == int(value):
            return int(value)
    except Exception:
        pass
    return value
def _get_operation(obj, op, ignore=False):
    method = getattr(obj,  op, None)
    if not method:
        if ignore:
            return lambda *a, **k: NotImplemented
        raise NotImplementedError("%r is missing method '%s'" % (obj.__class__,op))
    return method

class Neutral():
    """A neutral value when computed with other values."""
    def __add__(self, value):
        return value
    def __radd__(self, value):
        return value
    def __sub__(self, value):
        return -value
    def __rsub__(self, value):
        return value
    def __mul__(self, value):
        return value
    def __rmul__(self, value):
        return value
    def __truediv__(self, value):
        return value**-1
    def __rtruediv__(self, value):
        return value
    def __repr__(self):
        return "<NEUTRAL>"
    def __str__(self):
        return "1"
    def __hash__(self) -> int:
        return hash(self.__class__)+1
Neutral.NEUTRAL = Neutral()


################################################################################
# DIMENSION                                                                    #
################################################################################

class Dimension(dict):
    """Relates to a physical dimension. Should be immutable."""
    def __new__(cls, *args, **kwds):
        obj = super(__class__, cls).__new__(cls)
        return obj
    def __init__(self, *args, **kwds):
        for i,arg in enumerate(args):
            if isinstance(arg, Unit):
                args[i] = arg.dim
            elif isinstance(arg, Quantity):
                args[i] = arg.unit.dim
        super(__class__, self).__init__(*args, **kwds)
        self.__prune()
    @classmethod
    def dim_of(cls, value):
        """Get the dimension of a value."""
        if isinstance(value, __class__): return value
        if isinstance(value, Unit): return cls.dim_of(value.dim)
        if isinstance(value, Quantity): return cls.dim_of(value.unit)
        return cls.dim_of(cls.NODIM)
    def copy(self):
        return __class__(self)
    def __prune(self):
        """remove useless indexes"""
        key_to_del = set()
        for key, value in super(__class__,self).items():
            if not value: key_to_del.add(key)
            else: super(__class__,self).__setitem__(key, _neatscale(value))
        for key in key_to_del:
            super(__class__,self).__delitem__(key)

    def __getitem__(self, key):
        if super(__class__,self).__contains__(key):
            return super(__class__,self).__getitem__(key)
        return 0
    def __setitem__(self, key, value):
        raise TypeError(
            "'%s' object does not support item assignment"%(self.__class__.__name__)
        )
        # if value:
        #     return super(__class__,self).__setitem__(key, value)
        # if super(__class__,self).__contains__(key):
        #     return super(__class__,self).__delitem__(key)
    def __delitem__(self, key):
        raise TypeError(
            "'%s' object does not support item deletion"%(self.__class__.__name__)
        )
        # return super(__class__,self).__delitem__(key)
    def __getattr__(self, *arg,**kwd):
        return self.__getitem__(*arg,**kwd)
    def __setattr__(self, *arg,**kwd):
        return self.__setitem__(*arg,**kwd)
    def __delattr__(self, *arg,**kwd):
        return self.__delitem__(*arg,**kwd)
    def pop(self, *arg,**kwd):
        raise TypeError(
            "'%s' object does not support item deletion"%(self.__class__.__name__)
        )
    def popitem(self, *arg,**kwd):
        raise TypeError(
            "'%s' object does not support item deletion"%(self.__class__.__name__)
        )
    @functools.lru_cache(maxsize=32)
    def items(self):
        return sorted(
            super(__class__,self).items(),
            key=lambda item: (item[1]<0, abs(item[1]), item[0])
        )

    def __r_binary_op(self, value, op):
        if not isinstance(value, __class__): return NotImplemented
        return _get_operation(value, op)(self)

    """__add__ and co only perform dimensionality check"""
    def __neg__(self):
        return self
        # return self.copy()
    def __add__(self, value):
        # if not isinstance(value, __class__): return NotImplemented
        dim = self.dim_of(value)
        if self != dim: raise DimensionError.from_dims(self, dim)
        return value
        # return value.copy()
    # def __radd__(self,value): return self.__r_binary_op(value, '__add__')
    def __radd__(self,value): return self.__add__(value)
    def __sub__(self,value):  return self.__add__(-value)
    def __rsub__(self,value): return (-self).__radd__(value)

    @functools.lru_cache(maxsize=32)
    def __mul__(self, value):
        if not isinstance(value, __class__): return NotImplemented
        if not self: return value
        if not value: return self
        ans = self.copy()
        for k,v in value.items():
            super(__class__,ans).__setitem__(k, ans[k]+v)
        ans.__prune()
        return ans
    def __rmul__(self,value): return self.__r_binary_op(value, '__mul__')
    @functools.lru_cache(maxsize=32)
    def __truediv__(self, value):
        if not isinstance(value, __class__): return NotImplemented
        if not value: return self
        if self is value: return __class__.NODIM
        ans = self.copy()
        for k,v in value.items():
            super(__class__,ans).__setitem__(k, ans[k]-v)
        ans.__prune()
        return ans
    def __rtruediv__(self,value):  return self.__r_binary_op(value, '__truediv__')
    def __floordiv__(self,value):
        if not isinstance(value, __class__): return NotImplemented
        if self != value: raise DimensionError.from_dims(self, value)
        return __class__.NODIM
    def __rfloordiv__(self,value): return self.__r_binary_op(value, '__floordiv__')
    def __mod__(self, value):
        if not isinstance(value, __class__): return NotImplemented
        if self != value: raise DimensionError.from_dims(self, value)
        return self
        # return value.copy()
    def __rmod__(self,value): return self.__rtruediv__(value)
    def __divmod__(self,value):
        if not isinstance(value, __class__): return NotImplemented
        return (self.__floordiv__(value), self.__mod__(value))
    def __rdivmod__(self,value):  return self.__r_binary_op(value, '__divmod__')
    @functools.lru_cache(maxsize=32)
    def __pow__(self, value):
        if not self: return self
        ans = self.copy()
        for k,v in self.items():
            super(__class__,ans).__setitem__(k, v*value)
        ans.__prune()
        return ans

    def __eq__(self,value):
        return super(__class__,self).__eq__(value)
    def __lt__(self, value):
        if not isinstance(value, __class__): return NotImplemented
        if self != value: raise DimensionError.from_dims(self, value)
        return NotImplemented
    def __le__(self,value): return self.__lt__(value)
    def __gt__(self,value): return self.__lt__(value)
    def __ge__(self,value): return self.__lt__(value)
    def __hash__(self) -> int:
        ans = 0
        for k,v in super(__class__,self).items():
            hash_v = hash(v)
            if v==-1 and hash_v==-2:
                hash_v = -1
            ans += hash(k)*hash_v
        return ans*hash(self.__class__)

    def __str__(self) -> str:
        from . import params
        formatter = params.get('str_formatter')
        if formatter is None: return super().__str__()
        return formatter.format(self)
    def __repr__(self) -> str:
        from . import params
        formatter = params.get('repr_formatter')
        if formatter is None: return super().__repr__()
        return formatter.format(self)
    def _repr_mimebundle_(self, *args, **kwargs):
        """For IPython."""
        from . import formatters
        return formatters.repr_mimebundle(self, *args, **kwargs)
    # def _repr_latex_(self):
    #     """For IPython."""
    #     from . import formatters
    #     return formatters.LatexFormatter().repr_mimetype(self)

Dimension.NODIM = Dimension()


################################################################################
# UNIT                                                                         #
################################################################################

@ordering(
    key=lambda obj: (obj.dim,obj.scale)
)
class Unit(object):
    """Describes a physical unit. Should be immutable."""
    __match_args__ = ('scale','dim',)
    def __init__(self, *args, scale=Neutral.NEUTRAL, dim=Dimension.NODIM, **kwds):
        """Create a new Unit with a dimension and a certain scale."""
        if not isinstance(dim, Dimension):
            dim = Dimension(dim)
        if kwds:
            dim *= Dimension(**kwds)
        for arg in args:
            if isinstance(arg, Dimension):
                dim *= arg
            elif isinstance(arg, __class__):
                scale *= arg.scale
                dim *= arg.dim
            elif isinstance(arg, Quantity):
                scale *= arg.amount * arg.unit.scale
                dim *= arg.unit.dim
            else:
                scale *= arg
        if scale is Neutral.NEUTRAL:
            from . import params
            scale = params.get('_base_scale', Fraction(1))
        super(__class__, self).__init__()
        super(__class__, self).__setattr__('scale', scale)
        super(__class__, self).__setattr__('dim', dim)
    def __setattr__(self, name, value):
        raise TypeError(
            "'%s' object does not support attribute assignment"%(self.__class__.__name__)
        )
    def __delattr__(self, name):
        raise TypeError(
            "'%s' object does not support attribute deletion"%(self.__class__.__name__)
        )

    def __add__(self, value):
        if isinstance(value, Dimension): return NotImplemented  # let Dimension handle it
        self.dim + Dimension.dim_of(value)
        return value
    def __sub__(self, value):
        if isinstance(value, Dimension): return NotImplemented  # let Dimension handle it
        self.dim - Dimension.dim_of(value)
        return -value
    def __mul__(self, value):
        if not isinstance(value, __class__):
            value = __class__(value)
        return __class__(scale=_neatscale(self.scale*value.scale), dim=self.dim*value.dim)
    def __truediv__(self, value):
        if not isinstance(value, __class__):
            value = __class__(value)
        return __class__(scale=_neatscale(self.scale/value.scale), dim=self.dim/value.dim)
    def __pow__(self, value):
        return __class__(scale=_neatscale(self.scale**value), dim=self.dim**value)

    def __radd__(self, value):
        if not isinstance(value, (Unit,Quantity,Dimension)):
            value = Quantity(value)
        return value.__add__(self)
    def __rsub__(self, value):
        if not isinstance(value, (Unit,Quantity,Dimension)):
            value = Quantity(value)
        return value.__sub__(self)
    def __rmul__(self, value):
        if not isinstance(value, (Unit,Quantity)):
            value = Quantity(value)
        return value.__mul__(self)
    def __rtruediv__(self, value):
        if not isinstance(value, (Unit,Quantity)):
            value = Quantity(value)
        return value.__truediv__(self)
    def __rfloordiv__(self, value):
        if not isinstance(value, (Unit,Quantity)):
            value = Quantity(value)
        return value.__floordiv__(self)
    def __rmod__(self, value):
        if not isinstance(value, (Unit,Quantity)):
            value = Quantity(value)
        return value.__mod__(self)
    def __rdivmod__(self,value):
        if not isinstance(value, (Unit,Quantity)):
            value = Quantity(value)
        return value.__divmod__(self)

    def __hash__(self) -> int:
        ans = hash(self.scale) + hash(self.dim)
        return ans*hash(self.__class__)

    def __bool__(self) -> bool:
        """Returns True if it is distinct from the unitary dimensionless unit."""
        return bool(self.dim) or self.scale not in (1,Neutral.NEUTRAL)
    def __str__(self) -> str:
        from . import params
        formatter = params.get('str_formatter')
        if formatter is None: return super().__str__()
        return formatter.format(self)
    def __repr__(self) -> str:
        from . import params
        formatter = params.get('repr_formatter')
        if formatter is None: return super().__repr__()
        return formatter.format(self)
    def _repr_mimebundle_(self, *args, **kwargs):
        """For IPython."""
        from . import formatters
        return formatters.repr_mimebundle(self, *args, **kwargs)
    # def _repr_latex_(self):
    #     """For IPython."""
    #     from . import formatters
    #     return formatters.LatexFormatter().repr_mimetype(self)

Unit.SCALAR = Unit()


################################################################################
# QUANTITY                                                                     #
################################################################################

@ordering(
    key=(lambda obj: (obj.unit.dim,obj.amount*obj.unit.scale)),
    standard=(lambda other: Quantity(other) if not isinstance(other,(Dimension,Unit,Quantity)) else other),
)
class Quantity(object):
    """Describes a certain amount of a given unit."""
    __match_args__ = ('amount','unit',)
    def __init__(self, *args, amount=Neutral.NEUTRAL, unit=Unit.SCALAR):
        """Create a new Unit with a dimension and a certain scale."""
        for arg in args:
            if isinstance(arg, Dimension):
                raise TypeError(
                    "%s does not accept %s as argument" % (
                        self.__class__.__name__,
                        arg.__class__.__name__,
                    )
                )
            elif isinstance(arg, Unit):
                unit *= arg
            elif isinstance(arg, __class__):
                amount *= arg.amount
                unit *= arg.unit
            else:
                amount *= arg
        if amount is Neutral.NEUTRAL:
            amount = 0
        super(__class__, self).__init__()
        super(__class__, self).__setattr__('amount', amount)
        super(__class__, self).__setattr__('unit', unit)
    def copy(self):
        ans = self.__class__(self)
        if getattr(ans.amount, 'copy', None) is not None:
            ans.amount = ans.amount.copy()
        return ans

    def _return_scalar(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwds):
            ans = fun(*args, **kwds)
            from . import params
            if params.get('unwrap_scalar',True) and isinstance(ans, __class__) and not ans.unit:
                ans = ans.amount
            return ans
        return wrapper

    def convert(self, unit=None):
        """Convert quantity in place from a unit to an other unit.
        If unit is not specified, convert to SI."""
        if unit is None and isinstance(self.unit.scale, Fraction): unit = Unit(Fraction(1), self.unit.dim)
        if unit is None: unit = Unit(self.unit.dim)
        if self.unit is unit or self.unit == unit: return self
        factor = (self.unit/unit).scale
        self.unit += unit
        if factor==1: return self
        self.amount = _neatscale(self.amount*factor)
        return self
    @_return_scalar
    def __add__(self, value):
        if isinstance(value, Dimension): return NotImplemented  # let Dimension handle it
        ans = self.copy()
        ans.__iadd__(value) # /!\ ans.amount += value.amount
        return ans
    def __iadd__(self, value):
        if isinstance(value, Dimension): return NotImplemented  # let Dimension handle it
        if isinstance(value, Unit):
            self.convert(value)
            return self
        if isinstance(value, Dimension):
            return self
        if not isinstance(value, __class__):
            value = __class__(value)
        self.convert(value.unit)
        self.amount += value.amount
        return self
    @_return_scalar
    def __pos__(self):
        ans = self.copy()
        ans.amount = +ans.amount
        return ans
    @_return_scalar
    def __sub__(self, value):
        if isinstance(value, Dimension): return NotImplemented  # let Dimension handle it
        ans = self.copy()
        ans.__isub__(value) # /!\ ans.amount -= value.amount
        return ans
    def __isub__(self, value):
        if isinstance(value, Dimension): return NotImplemented  # let Dimension handle it
        if isinstance(value, Unit):
            self.convert(value)
            return self
        if not isinstance(value, __class__):
            value = __class__(value)
        self.convert(value.unit)
        self.amount -= value.amount
        return self
    @_return_scalar
    def __neg__(self):
        ans = self.copy()
        ans.amount = -ans.amount
        return ans
    @_return_scalar
    def __mul__(self, value):
        ans = self.copy()
        ans.__imul__(value) # /!\ ans.amount *= value.amount
        return ans
    def __imul__(self, value):
        if isinstance(value, Unit):
            self.unit *= value
            return self
        if not isinstance(value, __class__):
            value = __class__(value)
        self.amount *= value.amount
        self.unit *= value.unit
        return self
    @_return_scalar
    def __truediv__(self, value):
        ans = self.copy()
        ans.__itruediv__(value) # /!\ ans.amount /= value.amount
        return ans
    def __itruediv__(self, value):
        if isinstance(value, Unit):
            self.unit /= value
            return self
        if not isinstance(value, __class__):
            value = __class__(value)
        self.amount /= value.amount
        self.unit /= value.unit
        return self
    @_return_scalar
    def __floordiv__(self, value) -> int:
        ans = self.copy()
        ans.__ifloordiv__(value) # /!\ ans.amount //= value.amount
        return ans
    def __ifloordiv__(self, value):
        if isinstance(value, Unit):
            value = __class__(amount=1, unit=value)
        if not isinstance(value, __class__):
            value = __class__(value)
        self.convert(value.unit)
        self.amount //= value.amount
        try: self.amount = round(self.amount)
        except (ValueError, ArithmeticError): pass
        self.unit /= value.unit
        return self
    @_return_scalar
    def __mod__(self, value):
        ans = self.copy()
        ans.__imod__(value) # /!\ ans.amount %= value.amount
        return ans
    def __imod__(self, value):
        if isinstance(value, Unit):
            value = __class__(amount=1, unit=value)
        if not isinstance(value, __class__):
            value = __class__(value)
        self.convert(value.unit)
        self.amount %= value.amount
        return self
    def __divmod__(self,value):
        if isinstance(value, Unit):
            value = __class__(amount=1, unit=value)
        if not isinstance(value, __class__):
            value = __class__(value)
        a = self.copy()
        a.convert(value.unit)
        b = a.copy()
        a.amount, b.amount = divmod(a.amount,value.amount)
        try: a.amount = round(a.amount)
        except (ValueError, ArithmeticError): pass
        a.unit /= value.unit
        if not a.unit: a = a.amount
        if not b.unit: b = b.amount
        return (a,b)
    @_return_scalar
    def __pow__(self, value):
        ans = self.copy()
        ans.__ipow__(value) # /!\ ans.amount **= value.amount
        return ans
    def __ipow__(self, value):
        self.amount **= value
        self.unit **= value
        return self

    def __radd__(self, value):
        if not isinstance(value, (Unit,Quantity,Dimension)):
            value = Quantity(value)
        return value.__add__(self)
    def __rsub__(self, value):
        if not isinstance(value, (Unit,Quantity,Dimension)):
            value = Quantity(value)
        return value.__sub__(self)
    def __rmul__(self, value):
        if not isinstance(value, (Unit,Quantity)):
            value = Quantity(value)
        return value.__mul__(self)
    def __rtruediv__(self, value):
        if not isinstance(value, (Unit,Quantity)):
            value = Quantity(value)
        return value.__truediv__(self)
    def __rfloordiv__(self, value):
        if not isinstance(value, (Unit,Quantity)):
            value = Quantity(value)
        return value.__floordiv__(self)
    def __rmod__(self, value):
        if not isinstance(value, (Unit,Quantity)):
            value = Quantity(value)
        return value.__mod__(self)
    def __rdivmod__(self, value):
        if not isinstance(value, (Unit,Quantity)):
            value = Quantity(value)
        return value.__divmod__(self)
    def __abs__(self):
        ans = self.copy()
        ans.amount = abs(ans.amount)
        return ans
    @_return_scalar
    def __floor__(self):
        import math
        ans = self.copy()
        ans.amount = math.floor(ans.amount)
        return ans
    @_return_scalar
    def __ceil__(self):
        import math
        ans = self.copy()
        ans.amount = math.ceil(ans.amount)
        return ans
    @_return_scalar
    def __round__(self, ndigits=None):
        ans = self.copy()
        ans.amount = round(ans.amount, ndigits=ndigits)
        return ans
    def __int__(self) -> int:
        ans = self.copy()
        ans.convert(Unit.SCALAR)
        return int(ans.amount)
    def __float__(self) -> float:
        ans = self.copy()
        ans.convert(Unit.SCALAR)
        return float(ans.amount)
    def __bool__(self) -> bool:
        return bool(self.amount)
    __nonzero__ = __bool__

    def __hash__(self) -> int:
        ans = hash(self.amount) + hash(self.unit)
        return ans*hash(self.__class__)

    def __str__(self) -> str:
        from . import params
        formatter = params.get('str_formatter')
        if formatter is None: return super().__str__()
        return formatter.format(self)
    def __repr__(self) -> str:
        from . import params
        formatter = params.get('repr_formatter')
        if formatter is None: return super().__repr__()
        return formatter.format(self)
    def _repr_mimebundle_(self, *args, **kwargs):
        """For IPython."""
        from . import formatters
        return formatters.repr_mimebundle(self, *args, **kwargs)
    # def _repr_latex_(self):
    #     """For IPython."""
    #     from . import formatters
    #     return formatters.LatexFormatter().repr_mimetype(self)

    del _return_scalar


__all__ = ["Dimension", "Unit", "Quantity"]
