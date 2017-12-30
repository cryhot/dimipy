#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools

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

class ConversionError(TypeError):
    """Inappropriate dimention."""
    def __init__(self, *args, **kwds):
        super(ConversionError, self).__init__(*args, **kwds)
    @classmethod
    def from_dims(cls, from_, to):
        """Create and return a new ConversionError from two dimentions."""
        return cls("Inhomogeneous conversion from [%s] to [%s]"%(from_, to))
    # def from_units(from_, to):
    #     """Create and return a new ConversionError from two units."""
    #     return ConversionError("Inhomogeneous conversion from '%r' to '%r'"%(from_, to))

def _neatscale(value):
    """Transform a value in a neater value"""
    try:
        if value == int(value):
            return int(value)
    except Exception:
        pass
    return value
_tran_exposant = str.maketrans(
    "0123456789+-=().",
    "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾·",
)
_tran_indice = str.maketrans(
    "0123456789+-e=().",
    "₀₁₂₃₄₅₆₇₈₉₊₋ₑ₌₍₎.",
)
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
    def __hash__(self):
        return hash(self.__class__)+1
Neutral.NEUTRAL = Neutral()


################################################################################
# DIMENTION                                                                    #
################################################################################

class Dimention(dict):
    """Relates to a physical dimention. Should be immutable."""
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
        """Get the dimention of a value."""
        if isinstance(value, cls): return value
        if isinstance(value, Unit): return value.dim
        if isinstance(value, Quantity): return value.unit.dim
        return cls.NODIM
    def copy(self):
        return __class__(self)
    def __prune(self):
        """remove useless indexes"""
        key_to_del = set()
        for key, value in super(__class__,self).items():
            if not value: key_to_del.add(key)
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
        raise NotImplementedError()
    def popitem(self, *arg,**kwd):
        raise NotImplementedError()
    @functools.lru_cache(maxsize=32)
    def items(self):
        return sorted(
            super(__class__,self).items(),
            key=lambda item: (item[1]<0, abs(item[1]), item[0])
        )

    def __r_binary_op(self, value, op):
        if not isinstance(value, self.__class__): return NotImplemented
        return _get_operation(value, op)(self)

    def __neg__(self):
        return self
        # return self.copy()
    def __add__(self, value):
        if not isinstance(value, self.__class__): return NotImplemented
        if self != value: raise ConversionError.from_dims(self, value)
        return value
        # return value.copy()
    def __radd__(self,value): return self.__r_binary_op(value, '__add__')
    def __sub__(self,value):  return self.__add__(value)
    def __rsub__(self,value): return self.__radd__(value)
    @functools.lru_cache(maxsize=32)
    def __mul__(self, value):
        if not isinstance(value, self.__class__): return NotImplemented
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
        if not isinstance(value, self.__class__): return NotImplemented
        if not value: return self
        if self is value: return __class__.NODIM
        ans = self.copy()
        for k,v in value.items():
            super(__class__,ans).__setitem__(k, ans[k]-v)
        ans.__prune()
        return ans
    def __rtruediv__(self,value):  return self.__r_binary_op(value, '__truediv__')
    def __floordiv__(self,value):
        if not isinstance(value, self.__class__): return NotImplemented
        if self != value: raise ConversionError.from_dims(self, value)
        return __class__.NODIM
    def __rfloordiv__(self,value): return self.__r_binary_op(value, '__floordiv__')
    def __mod__(self, value):
        if not isinstance(value, self.__class__): return NotImplemented
        if self != value: raise ConversionError.from_dims(self, value)
        return self
        # return value.copy()
    def __rmod__(self,value): return self.__rtruediv__(value)
    def __divmod__(self,value):
        if not isinstance(value, self.__class__): return NotImplemented
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
        if not isinstance(value, self.__class__): return NotImplemented
        if self != value: raise ConversionError.from_dims(self, value)
        return NotImplemented
    def __le__(self,value): return self.__lt__(value)
    def __gt__(self,value): return self.__lt__(value)
    def __ge__(self,value): return self.__lt__(value)
    def __hash__(self):
        ans = 0
        for k,v in super(__class__,self).items():
            hash_v = hash(v)
            if v==-1 and hash_v==-2:
                hash_v = -1
            ans += hash(k)*hash_v
        return ans*hash(self.__class__)

    def repr_dim(self):
        if not self: return "1"
        return " ".join(
            "{}{}".format(
                k,
                repr(v).translate(_tran_exposant) if v!=1 else "",
            )
            for k,v in self.items()
        )
    def __repr__(self):
        return "{!s}[{}]".format(
            self.__class__.__name__,
            self.repr_dim(),
        )
    def __str__(self):
        if not self: return "1"
        return "".join(
            "{}{}".format(
                k,
                str(v).translate(_tran_exposant) if v!=1 else "",
            )
            for k,v in self.items()
        )

Dimention.NODIM = Dimention()


################################################################################
# UNIT                                                                         #
################################################################################

@ordering(
    key=lambda obj: (obj.dim,obj.scale)
)
class Unit(object):
    """Describes a physical unit. Should be immutable."""
    def __init__(self, *args, scale=Neutral.NEUTRAL, dim=Dimention.NODIM, **kwds):
        """Create a new Unit with a dimention and a certain scale."""
        if kwds:
            dim *= Dimention(**kwds)
        for arg in args:
            if isinstance(arg, Dimention):
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
            scale = 1
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
        self.dim + Dimention.dim_of(value)
        return value
    def __sub__(self, value):
        self.dim - Dimention.dim_of(value)
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
        if not isinstance(value, (Unit,Quantity)):
            value = Quantity(value)
        return value.__add__(self)
    def __rsub__(self, value):
        if not isinstance(value, (Unit,Quantity)):
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

    def __hash__(self):
        ans = hash(self.scale) + hash(self.dim)
        return ans*hash(self.__class__)

    def __bool__(self):
        return bool(self.dim) or self.scale not in (1,Neutral.NEUTRAL)
    def __repr__(self):
        return "{!s}[{!r} * {}]".format(
            self.__class__.__name__,
            self.scale,
            self.dim.repr_dim(),
        )
    def __str__(self):
        return "({!s}{!s})".format(
            self.scale,
            self.dim or "",
        )

Unit.SCALAR = Unit()


################################################################################
# QUANTITY                                                                     #
################################################################################

@ordering(
    key=(lambda obj: (obj.unit.dim,obj.amount*obj.unit.scale)),
    standard=(lambda other: Quantity(other) if not isinstance(other,(Dimention,Unit,Quantity)) else other),
)
class Quantity(object):
    """Describes a certain amount of a given unit."""
    def __init__(self, *args, amount=Neutral.NEUTRAL, unit=Unit.SCALAR):
        """Create a new Unit with a dimention and a certain scale."""
        for arg in args:
            if isinstance(arg, Dimention):
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
            if isinstance(ans, __class__) and not ans.unit:
                ans = ans.amount
            return ans
        return wrapper

    def convert(self, unit=None):
        """Convert quantity in place from a unit to an other unit.
        If unit is not specified, convert to SI."""
        if unit is None: unit = Unit(self.unit.dim)
        if self.unit is unit or self.unit == unit: return
        factor = (self.unit/unit).scale
        self.unit += unit
        if factor==1: return
        self.amount = _neatscale(self.amount*factor)
        return self
    @_return_scalar
    def __add__(self, value):
        ans = self.copy()
        ans.__iadd__(value) # /!\ ans.amount += value.amount
        return ans
    def __iadd__(self, value):
        if isinstance(value, Unit):
            self.convert(value)
            return self
        if not isinstance(value, __class__):
            value = __class__(value)
        self.convert(value.unit)
        self.amount += value.amount
        return self
    @_return_scalar
    def __sub__(self, value):
        ans = self.copy()
        ans.__isub__(value) # /!\ ans.amount -= value.amount
        return ans
    def __isub__(self, value):
        if isinstance(value, Unit):
            self.convert(value)
            return self
        if not isinstance(value, __class__):
            value = __class__(value)
        self.convert(value.unit)
        self.amount -= value.amount
        return self
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
    def __pow__(self, value):
        ans = self.copy()
        ans.__ipow__(value) # /!\ ans.amount **= value.amount
        return ans
    def __ipow__(self, value):
        self.amount **= value
        self.unit **= value
        return self

    def __radd__(self, value):
        if not isinstance(value, (Unit,Quantity)):
            value = Quantity(value)
        return value.__add__(self)
    def __rsub__(self, value):
        if not isinstance(value, (Unit,Quantity)):
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

    def __hash__(self):
        ans = hash(self.scale) + hash(self.dim)
        return ans*hash(self.__class__)

    def __repr__(self):
        return "{!s}[{!r} * ({!r} * {})]".format(
            self.__class__.__name__,
            self.amount,
            self.unit.scale,
            self.unit.dim.repr_dim(),
        )
    def __str__(self):
        return "{!s}{!s}".format(
            self.amount,
            self.unit,
        )

    del _return_scalar


__all__ = ["Dimention", "Unit", "Quantity"]
