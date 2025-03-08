#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import functools
from fractions import Fraction
from .core import Dimension, Unit, Quantity



class Formatter():
    _defaults = dict(
        dim_spacing = " ",
        amount_spacing = None,  # None: same as dim_spacing, str: custom spacing
        unit_color = True,  # False: deactivate, True: use params['unit_color'], str: custom color
        fractions = True, # None: allow native fractions, True: inference allowed, False: disable fractions
    )
    _default_spacing = 'dim_spacing'
    def __init__(self, **kwargs):
        for name,value in self._defaults.items():
            setattr(self, name, value)
        for name,value in kwargs.items():
            if name not in self._defaults:
                raise TypeError(f"{name!r} is an invalid parameter for {self.__class__.__qualname__}")
            setattr(self, name, value)
    def __repr__(self):
        kwargs = dict()
        for name, default in self._defaults.items():
            value = getattr(self, name)
            if value == default: continue
            kwargs[name] = value
        kwargs = ", ".join(f"{key}={value!r}" for key,value in kwargs.items())
        return f"{self.__class__.__qualname__}({kwargs})"
    def get_unit_color(self):
        color = getattr(self, 'unit_color', None)
        if isinstance(color, str): return color
        from . import params
        if color: color = params.get('unit_color')
        return color or None
    def spacing(self, mode="dim", *, ifnot:str=None, ifspace:str=None) -> str:
        """Retrieves `self.{mode}_spacing` or a default value.
        If the return value would be empty/only spaces, returns `ifnot`/`ifspace` instead if specified, respectively.
        """
        spacing = getattr(self, f'{mode}_spacing', self._defaults.get(f'{mode}_spacing', None))
        if spacing is None: spacing = getattr(self, self._default_spacing, self._defaults[self._default_spacing])
        if (not spacing) and ifnot is not None: spacing = ifnot
        elif (not spacing or spacing.isspace()) and ifspace is not None: spacing = ifspace
        return spacing

    _tran_superscript = str.maketrans(
        "0123456789+-=().",
        "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾·",
    )
    _tran_subscript = str.maketrans(
        "0123456789+-e=().",
        "₀₁₂₃₄₅₆₇₈₉₊₋ₑ₌₍₎.",
    )
    @classmethod
    def _unicode_superscript(cls, text:str) -> str:
        return text.translate(cls._tran_superscript)
    @classmethod
    def _unicode_subscript(cls, text:str) -> str:
        return text.translate(cls._tran_subscript)
    @staticmethod
    def format_class(cls) -> str:
        if not isinstance(cls, type): cls = cls.__class__
        # return f"{cls.__module__}.{cls.__qualname__}"
        return f"{cls.__qualname__}"
    def colored(self, text:str, color) -> str:
        if not color: return text
        try: import termcolor
        except ModuleNotFoundError: return text
        return termcolor.colored(text, color=color)
    def fmt_std(self,value,**kwargs):
        if isinstance(value,Fraction):
            fractions = getattr(self,'fractions',self._defaults.get('fractions', None))
            if fractions is None: fractions = True
            if not fractions: raise ValueError('fraction representation disabled')
        return self.format(value, **kwargs)
    def fmt_pow(self,value,base,log=None,**kwargs):
        """format as power of a base."""
        if log is None: log = functools.partial(math.log,base=base)
        e = log(value)
        if e == 0: raise ValueError("no need")
        exponent = int(e)
        if exponent != e: raise ValueError('no representation')
        return self.format_power(base, exponent)
    def fmt_f(self,value,d=4,**kwargs):
        """format as float with at most d digits."""
        value = float(value)
        if math.log10(value)<-15+d-1: raise ValueError('no accurate representation')
        v = f"{value:.15f}"
        v = v.rstrip("0")
        i_p = v.find('.')
        i_s = len(v)-len(v.lstrip("0.")) # index of first significant digit
        v = f"{float(v):.{max(0,min(i_s+d-i_p-(i_p<i_s),len(v)-i_p-1))}f}"
        return v
    def fmt_e(self,value,d=3,**kwargs):
        """format as exponent with at most d digits."""
        value = float(value)
        f,e = f"{value:.15e}".split('e')
        f = f.rstrip(".0")
        if len(f)>1+d: f = f"{float(f):.{d-1}f}"
        e = ("","-")[e.startswith("-")] + e.lstrip("+-0")
        return self.format_power(10,e,f)
    def fmt_frac(self,value,d=12,**kwargs):
        """format as fraction."""
        if isinstance(value, (int)): raise ValueError("no need")
        fractions = getattr(self,'fractions',self._defaults.get('fractions', None))
        if fractions is None: fractions = False
        if not fractions: raise ValueError('fraction inference disabled')
        v = Fraction(value)
        if not isinstance(value, Fraction):
            v = v.limit_denominator(10**d)
            if abs(v)<10**-(d-4): raise ValueError('no accurate representation')
        return self.format(v, **kwargs)
    def format_scale(self, value, **kwargs) -> str:
        """Print a value in a neater way. The shortest representation is returned."""
        answers = []
        fmts = [
            functools.partial(self.fmt_pow,base=10,log=math.log10),
            self.fmt_std,
            self.fmt_f,
            self.fmt_frac,
            self.fmt_e,
            functools.partial(self.fmt_pow,base=2,log=math.log2),
        ]
        for fmt in fmts:
            try: answers.append(fmt(value,**kwargs))
            except Exception: pass
        answers.sort(key=self.len_estimate)
        return answers[0]
    @staticmethod
    def len_estimate(text:str) -> float:
        """For comparing representation length."""
        return len(text)
    def format_power(self, base, exponent, factor=None) -> str:
        """formats (factor*(base**exponent))."""
        f = f"{factor!s}{self.spacing('dim',ifspace='*').strip()}"
        if factor is None: f = ""
        if factor==1: f = ""
        b = f"{base!s}"
        e = f"^{exponent!s}"
        if exponent == 1: e = ""
        return f"{f}{b}{e}"
    
    def format_dim(self, dim:Dimension) -> str:
        ans = self.spacing('dim').join(
            self.format_power(base, exponent)
            for base, exponent in dim.items()
        )
        if not ans: ans = "1"
        return ans
    def format_unit(self, unit:Unit) -> str:
        scale = self.format_scale(unit.scale)
        dim = self.spacing('dim')+self.format_dim(unit.dim) if unit.dim else ""
        return f"{scale}{dim}"
    def format_quantity(self, quantity:Quantity) -> str:
        amount = f"{quantity.amount!s}"
        unit = f"{self.spacing('amount')}({self.format_unit(quantity.unit)})"
        unit = self.colored(unit, self.get_unit_color())
        return f"{amount}{unit}"

    def format(self, value) -> str:
        if   isinstance(value, Dimension): ans = f"[{self.format_dim(value)}]"
        elif isinstance(value, Unit):      ans = f"({self.format_unit(value)})"
        elif isinstance(value, Quantity):  ans = f"{self.format_quantity(value)}"
        else:
            ans = str(value)
        if isinstance(value, (Dimension,Unit)): ans = self.colored(ans, self.get_unit_color())
        return ans
    
    mimetype = "text/plain"
    def repr_mimetype(self, value):
        """For IPython."""
        return self.format(value)
    def Display(self, value):
        """For IPython.
        >>> IPython.display.display(formatter.Display(value))
        """
        return Display(self,value)

class PrettyFormatter(Formatter):
    _defaults = Formatter._defaults.copy()
    _defaults.update(
        dim_spacing = "",
    )
    def format_power(self, base, exponent, factor=None) -> str:
        f = f"{factor!s}{self.spacing('dim',ifspace='⋅').strip()}"
        if factor is None: f = ""
        if factor==1: f = ""
        b = f"{base!s}"
        e = self._unicode_superscript(f"{exponent!s}")
        if exponent == 1: e = ""
        return f"{f}{b}{e}"


class LegacyFormatter(PrettyFormatter):
    _defaults = Formatter._defaults.copy()
    _defaults.update(
        dim_spacing = " ",
        amount_spacing = " * ",
    )
    def format_unit(self, unit:Unit) -> str:
        scale = self.format_scale(unit.scale)
        dim = self.format_dim(unit.dim)
        return f"{scale}{self.spacing('amount')}{dim}"

    def format(self, value) -> str:
        if   isinstance(value, Dimension): ans = f"{self.format_class(value)}[{self.format_dim(value)}]"
        elif isinstance(value, Unit):      ans = f"{self.format_class(value)}[{self.format_unit(value)}]"
        elif isinstance(value, Quantity):  ans = f"{self.format_class(value)}[{self.format_quantity(value)}]"
        else:
            ans = str(value)
        if isinstance(value, (Dimension,Unit)): ans = self.colored(ans, self.get_unit_color())
        return ans
        


class LatexFormatter(Formatter):
    _defaults = Formatter._defaults.copy()
    _defaults.update(
        dim_spacing = "",
        # dim_spacing = r"\cdot",
        # amount_spacing = r"\ ",
    )
    def colored(self, text, color):
        if not color: return text
        return r"{\color{%s}%s}" % (color, text)
    @staticmethod
    def len_estimate(text:str) -> float:
        import re
        text = re.sub(r"\\(cdot|times)", "+", text)
        text = re.sub(r"\\color{([^}]*)}", "", text)
        text = re.sub(r"\\frac{([^}]*)}{([^}]*)}", lambda m: max(m.groups(),key=len), text)  # keep larger text
        text = re.sub(r"\\[a-zA-Z]+", "", text)  # ignore other functions
        text = re.sub(r"[{}^_]", "", text)
        return len(text)
    def format_power(self, base, exponent, factor=None) -> str:
        f = f"{factor!s}{self.spacing('dim',ifspace=chr(92)+'cdot')}"
        if factor is None: f = ""
        if factor==1: f = ""
        b = r"{%s}" % base
        if isinstance(base, str) and not base[:1].isdigit(): b = r"\mathsf{%s}" % base
        e = r"^{%s}" % self.format(exponent,mode='math')
        if exponent==1: e = ""
        return f"{f}{b}{e}"
    def format_unit(self, unit:Unit) -> str:
        scale = self.format_scale(unit.scale, mode='math')
        dim = self.spacing('dim')+self.format_dim(unit.dim) if unit.dim else ""
        return f"{scale}{dim}"
    def format_quantity(self, quantity:Quantity) -> str:
        amount = self.format(quantity.amount, mode='math')
        unit = self.format(quantity.unit, mode='math')
        return f"{amount}{self.spacing('amount')}{unit}"

    def format(self, value, *, mode='paragraph') -> str:
        inner_mode = 'math'
        if   isinstance(value, Dimension): tex = r"\left[%s\right]" % self.format_dim(value)
        elif isinstance(value, Unit):      tex = r"\left(%s\right)" % self.format_unit(value)
        elif isinstance(value, Quantity):  tex = r"%s" % self.format_quantity(value)
        elif isinstance(value, Fraction):
            if value.denominator == 1: tex = r"%s" % value.numerator
            else: tex = r"\frac{%s}{%s}" % (value.numerator, value.denominator)
        elif hasattr(value, '_repr_latex_'):
            tex = value._repr_latex_()
            inner_mode = 'paragraph'
        else:
            tex = str(value)
            # TODO: be more robust when escaping latex
            tex = tex.replace("\\",r"\\").replace("$", r"\$")
            inner_mode = 'paragraph'
            if isinstance(value, (int,float)) and mode=='math': inner_mode = 'math'
        if isinstance(value, (Dimension,Unit)): tex = self.colored(tex, self.get_unit_color())
        
        if mode == inner_mode: pass
        elif mode == 'math':
            # TODO: be more robust when stripping math markups, eg $$...$$, \(...\)
            if tex.startswith("$"): tex = tex.strip("$")
            else: tex = r"\text{%s}" % tex
        elif inner_mode == 'math':
            tex = r"$%s$" % tex
        return tex
    mimetype = "text/latex"
    def repr_mimetype(self, value):
        """For IPython."""
        # return r"$\displaystyle %s$" % self.format(value,mode='math')
        return self.format(value)

class CodeFormatter(Formatter):
    """Shows an executable code."""
    _defaults = Formatter._defaults.copy()
    _defaults.update(
        arg_spacing = " ",
        op_spacing = None, # "*" shall not be included
        explicit_type = False, # show the type of the object explicitly
        unit_color = False,
    )
    _defaults.pop('fractions',None)
    _default_spacing = 'arg_spacing'
    _defaults.pop('dim_spacing',None)
    @property
    def dim_spacing(self):
        return f",{self.spacing('arg')}"
    _defaults.pop('amount_spacing',None)
    @property
    def amount_spacing(self):
        return f"{self.spacing('op')}*{self.spacing('op')}"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for name in ['arg','op']:
            # check for true spacing (or no spacing)
            if self.spacing(name,ifspace="_")!="_":
                raise ValueError(f"invalid {name}_spacing: {self.spacing('name')!r}")

    @staticmethod
    def _isidentifier(key) -> bool:
        if not isinstance(key, str): return False
        if not key.isidentifier(): return False
        import keyword
        if key in keyword.kwlist: return False
        return True

    def format_dim(self, dim:Dimension) -> str:
        str_kwargs = []
        str_items = []
        # itemize = any(not self._isidentifier(base) for base in dim.keys())
        itemize = False
        for base, exponent in dim.items():
            if itemize or not self._isidentifier(base):
                str_items.append(f"{base!r}:{exponent!r}")
            else:
                str_kwargs.append(f"{base!s}={exponent!r}")
        if str_items:
            str_kwargs.append("**{%s}" % self.spacing('dim').join(str_items))
        return self.spacing('dim').join(str_kwargs)
    def format_unit(self, unit:Unit) -> str:
        str_args = [repr(unit.scale)]
        if unit.dim: str_args.append(self.format_dim(unit.dim))
        return self.spacing('dim').join(str_args)
    def format_quantity(self, quantity:Quantity) -> str:
        if self.explicit_type:
            str_args = [repr(quantity.amount), self.format(quantity.unit)]
            return self.spacing('dim').join(str_args)
        else:
            times = self.spacing('amount')
            times = self.colored(times, self.get_unit_color())
            return f"{quantity.amount!r}{times}{self.format(quantity.unit)}"
    
    def format(self, value) -> str:
        if   isinstance(value, Dimension): ans = f"{self.format_class(value)}({self.format_dim(value)})"
        elif isinstance(value, Unit):      ans = f"{self.format_class(value)}({self.format_unit(value)})"
        elif isinstance(value, Quantity):
            if self.explicit_type:         ans = f"{self.format_class(value)}({self.format_quantity(value)})"
            else:                          ans = f"{self.format_quantity(value)}"
        else:
            ans = str(value)
        if isinstance(value, (Dimension,Unit)): ans = self.colored(ans, self.get_unit_color())
        return ans


def repr_mimebundle(obj, include=None, exclude=None, *, formatter=None):
    """For IPython."""
    datas, metadatas = {}, {}
    from . import params
    formatters = formatter
    if formatters is None: formatters = params.get('display_formatter')
    if formatters is None: raise NotImplementedError()
    if isinstance(formatters, Formatter): formatters = (formatters,)
    for formatter in formatters:
        metadata = None
        data = formatter.repr_mimetype(obj)
        if isinstance(data, tuple): data, metadata = data
        datas[formatter.mimetype] = data
        if metadata is not None: metadatas[formatter.mimetype] = metadata
    return datas, metadata

class Display:
    """For IPython.
    >>> IPython.display.display(Display(formatter,value))
    """
    def __init__(self, formatter:Formatter, value):
        self.formatter = formatter
        self.value = value
    def __str__(self) -> str:
        return self.formatter.format(self.value)
    def __repr__(self) -> str:
        return self.formatter.format(self.value)
    def _repr_mimebundle_(self, *args, **kwargs):
        """For IPython."""
        return repr_mimebundle(self.value, *args, **kwargs, formatter=self.formatter)