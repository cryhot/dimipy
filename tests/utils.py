#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test dependency utils"""
import sys, os
import pytest

import dep


main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
sys.path.append(main_dir)
libname = "src"

@pytest.fixture(scope='session')
def self():
    """dummy fixture, to make it easy to move tests in and out of functions"""
    return None

