#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test dependency utils"""
import pytest
import contextlib
import importlib
import builtins

import os, glob

def fail(reason:str=""):
    """Abort the test because dependency is missing."""
    args = ["dependency"]
    if reason: args.append(reason)
    reason = ": ".join(args)
    return pytest.xfail(reason)
    return pytest.fail(reason)
    # return pytest.skip(reason)

contextlib.suppress
@contextlib.contextmanager
def suppress(*exceptions, reason="", pytrace=True):
    """Context manager to fail dependencies when specified exceptions occurs."""
    if not exceptions: exceptions = (BaseException,)
    try:
        yield
    except exceptions as err:
        args = []
        if reason: args.append(reason)
        if pytrace and str(err): args.append(str(err))
        reason = ": ".join(args)
        fail(reason)

def import_module(module_name:str):
    # return pytest.importorskip(module_name)
    # try: return importlib.import_module(module_name)
    # except Exception as err: fail(f"could not import '{module_name}': {err}")
    with suppress(reason="could not import"):
        return importlib.import_module(module_name)

def getattr(*args, **kwargs):
    with suppress():
        return builtins.getattr(object, *args, **kwargs)



