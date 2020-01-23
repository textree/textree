#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform
vers = platform.python_version_tuple()
import os,sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
if   2 >= int(vers[0]): from .py2.textree import *
elif 3 <= int(vers[0]): from .py3.textree import *
else: raise Exception('There is no source code corresponding to the specified Python version.')
