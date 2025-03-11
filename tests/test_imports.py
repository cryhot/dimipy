#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from pytest_check import check

import sys
import importlib
import os, glob
from fractions import Fraction

from utils import *


def walk_libs(path:str, lib:str):
    """iter through valid lib names"""
    libdir = lib.replace('.', os.sep)
    if not libdir: raise ValueError("must specify root lib")
    if os.path.isdir(os.path.join(path,libdir)):
        pl = len(os.path.join(path,libdir))-len(libdir)
        for dirpath, dirnames, filenames in os.walk(os.path.join(path,libdir), followlinks=True):
            libpath = dirpath[pl:]
            for filename in sorted(filenames):
                name,ext = os.path.splitext(filename)
                if ext != ".py": continue
                if name == "__init__": name = libpath
                else: name = os.path.join(libpath,name)
                name = name.replace(os.sep, '.')
                yield name
            if "__pycache__" in dirnames: dirnames.remove("__pycache__")  # tell os.walk to skip this directory
    elif os.path.isfile(os.path.join(path,libdir+".py")):
        yield lib

@pytest.fixture(params=[
    *walk_libs(main_dir,f"{libname}"),
],scope=None)
def module_name(self,request): return request.param
@pytest.fixture(scope=None)
def module(self,module_name): return dep.import_module(module_name)

@pytest.fixture(scope='session')
def src(): return dep.import_module(f"{libname}")



def test_import(self,module_name):
    module = importlib.import_module(module_name)

def test_all_sane(self,module):
    __all__ = getattr(module,'__all__',[])
    for var_name in ['__file__','__name__']:
        if var_name in __all__:
            print(f"{module.__name__}.__all__ =",__all__)
            pytest.fail(reason=f"{module.__name__}.__all__ contains {var_name!r}")

@pytest.mark.parametrize('module_name', [
    *walk_libs(main_dir,f"{libname}.dimensions"),
    *walk_libs(main_dir,f"{libname}.prefixes"),
    *walk_libs(main_dir,f"{libname}.units"),
    *walk_libs(main_dir,f"{libname}.constants"),
])
class Test_predefined:
    def test_no_class(self,module,src):
        for name,value in module.__dict__.items():
            if isinstance(value,type):
                check.fail(reason=f"{module.__name__}.{name} is a {value.__class__.__qualname__}")
    def test_no_blacklisted(self,module,src):
        with dep.suppress():
            blacklist = (
                src,
                src.core,
            )
        for name,value in module.__dict__.items():
            if any(value is bv for bv in blacklist):
                check.fail(reason=f"{module.__name__}.{name} = {value!r}")
    

@pytest.mark.parametrize('module_name', [
    *walk_libs(main_dir,f"{libname}.dimensions"),
])
class Test_predefined_dimensions:
    def test_no_instance(self,module,src):
        with dep.suppress():
            blacklist_clss = (
                src.Unit,
                src.Quantity,
                int,float,Fraction,
            )
        for name,value in module.__dict__.items():
            if isinstance(value,blacklist_clss):
                pytest.fail(reason=f"{module.__name__}.{name}.__class__ = {value.__class__.__qualname__}")

@pytest.mark.parametrize('module_name', [
    *walk_libs(main_dir,f"{libname}.prefixes"),
    *walk_libs(main_dir,f"{libname}.units"),
])
class Test_predefined_units:
    def test_no_instance(self,module,src):
        with dep.suppress():
            blacklist_clss = (
                src.Dimension,
                src.Quantity,
                int,float,Fraction,
            )
            Quantity = src.Quantity
        for name,value in module.__dict__.items():
            if isinstance(value,Quantity):
                if name.startswith("zero_") and module.__name__.startswith(f"{libname}.units"):
                    continue  # skip constants for affine units
            if isinstance(value,blacklist_clss):
                check.fail(f"{module.__name__}.{name}.__class__ = {value.__class__.__qualname__}")

@pytest.mark.parametrize('module_name', [
    *walk_libs(main_dir,f"{libname}.constants"),
])
class Test_predefined_quantity:
    def test_no_instance(self,module,src):
        with dep.suppress():
            blacklist_clss = (
                src.Dimension,
                src.Unit,
            )
        for name,value in module.__dict__.items():
            if isinstance(value,blacklist_clss):
                check.fail(f"{module.__name__}.{name}.__class__ = {value.__class__.__qualname__}")



if __name__ == "__main__":
    # invokes `python3 -m pytest`
    sys.exit(pytest.main([
        __file__,
        # '-tb=no', '-v',
        # '-rNf', # Get rid of (E)rrors
        # '-rP',  # Show passed tests outputs
        # '-s',   # Show Output, do not capture
        *sys.argv[1:],
    ]))