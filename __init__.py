#!/usr/bin/env python3
# -*- coding: utf-8 -*-

_tran_exposant = str.maketrans(
    "0123456789+-=().",
    "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾·",
)
_tran_indice = str.maketrans(
    "0123456789+-e=().",
    "₀₁₂₃₄₅₆₇₈₉₊₋ₑ₌₍₎.",
)
class Dims(dict):
    def __init__(self, *args, **kwds):
        super(Dims, self).__init__(*args, **kwds)
        self.__prune()
    def copy(self):
        return Dims(self)
    def __prune(self):
        "remove useless indexes"
        key_to_del = set()
        for key, value in self.items():
            if not value: key_to_del.add(key)
        for key in key_to_del:
            super(Dims,self).__delitem__(key)

    def __getitem__(self, key):
        if super(Dims,self).__contains__(key):
            return super(Dims,self).__getitem__(key)
        return 0
    def __setitem__(self, key, value):
        if value:
            return super(Dims,self).__setitem__(key, value)
        if super(Dims,self).__contains__(key):
            return super(Dims,self).__delitem__(key)
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

    def __neg__(self):
        return self.copy()
    def __add__(self, value):
        if not isinstance(value, Dims): return NotImplemented
        if self != value:
            raise TypeError("unsuported dimensions for +: '%r' '%r'" % (self, value))
        return self.copy()
    __radd__ = __add__
    __sub__ = __add__
    __rsub__ = __add__
    def __mul__(self, value):
        if not isinstance(value, Dims): return NotImplemented
        ans = self.copy()
        for k,v in value.items():
            ans[k] += v
        return ans
    __rmul__ = __mul__
    def __truediv__(self, value):
        if not isinstance(value, Dims): return NotImplemented
        ans = self.copy()
        for k,v in value.items():
            ans[k] -= v
        return ans
    def __rtruediv__(self, value):
        if not isinstance(value, Dims): return NotImplemented
        return value.__div__(self)
    __divmod__ = __truediv__
    __rdivmod__ = __rtruediv__
    def __pow__(self, value):
        ans = self.copy()
        for k in self.keys():
            ans[k] *= value
        return ans

    def __repr__(self):
        if not self: return "1"
        return "*".join("{}{}".format(k,str(v).translate(_tran_exposant) if v!=1 else "")
            for k,v in sorted(
                self.items(),
                key=lambda item: (item[1]<0, abs(item[1]), item[0])
            )
        )
    def __str__(self):
        if not self: return "1"
        return "".join("{}{}".format(k,str(v).translate(_tran_exposant) if v!=1 else "")
            for k,v in sorted(
                self.items(),
                key=lambda item: (item[1]<0, abs(item[1]), item[0])
            )
        )

Scalar = Dims()


class Unit(object):
    """docstring for Unit."""
    def __new__(cls, *args, **kwds):
        obj = super(Unit, cls).__new__(cls)
        Unit.__init__(obj, *args, **kwds)
        if not obj.dims: return obj.value
        return obj
    def __init__(self, value=1, dims={}, **kwds):
        super(Unit, self).__init__()
        self.value = value
        self.dims = Dims(dims, **kwds)

    def __get_operation(obj, op, ignore=False):
        method = getattr(obj,  op)
        if not method:
            if ignore:
                return lambda *a, **k: NotImplemented
            raise NotImplementedError("%r is missing method '%s'" % (obj.__class__,op))
        return method

    def __unary_op(self, op):
        dim = Unit.__get_operation(self.dims,  op)()
        if dim is NotImplemented: return NotImplemented
        val = Unit.__get_operation(self.value, op, True)()
        if val is NotImplemented: return NotImplemented
        return Unit(val, dim)
    def __neg__(self):  return self.__unary_op('__neg__')

    def __binary_op(self, value, op):
        if isinstance(value, Unit):
            dim = value.dims
            val = value.value
        else:
            dim = Scalar
            val = value
        dim = Unit.__get_operation(self.dims, op)(dim)
        if dim is NotImplemented: return NotImplemented
        val = Unit.__get_operation(self.value, op, True)(val)
        if val is NotImplemented: return NotImplemented
        return Unit(val, dim)
    def __eq__(self, value):  return self.__binary_op(value, '__eq__')
    def __add__(self, value):  return self.__binary_op(value, '__add__')
    def __radd__(self, value): return self.__binary_op(value, '__radd__')
    def __sub__(self, value):  return self.__binary_op(value, '__sub__')
    def __rsub__(self, value): return self.__binary_op(value, '__rsub__')
    def __mul__(self, value):  return self.__binary_op(value, '__mul__')
    def __rmul__(self, value): return self.__binary_op(value, '__rmul__')
    def __truediv__(self, value):  return self.__binary_op(value, '__truediv__')
    def __rtruediv__(self, value): return self.__binary_op(value, '__rtruediv__')
    def __divmod__(self, value):  return self.__binary_op(value, '__divmod__')
    def __rdivmod__(self, value): return self.__binary_op(value, '__rdivmod__')
    def __pow__(self, value):
        dim = Unit.__get_operation(self.dims, '__pow__')(value)
        if dim is NotImplemented: return NotImplemented
        val = Unit.__get_operation(self.value, '__pow__', True)(value)
        if dim is NotImplemented: return NotImplemented
        return Unit(val, dim)

    def __repr__(self):
        return "[{!r}*{!r}]".format(self.value, self.dims)
    def __str__(self):
        return "{!s}{!s}".format(self.value, self.dims)
