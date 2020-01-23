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
__copyright__    = 'Copyright (C) 2020 ytyaru'
__version__      = '0.0.1'
__license__      = 'GNU Affero General Public License Version 3 (AGPL-3.0)'
__author__       = 'ytyaru'
__author_email__ = 'pypi1@outlook.jp'
__url__          = 'https://github.com/textree/textree'
__all__ = ['Node', 'RootNode', 'NodeList', 'Path', 'TexTree', 'LineAnalizer' \
, 'RootDeserializer'
, 'RootSerializer'
, 'NodeDeserializer'
, 'NodeSerializer'
, 'RootAttributeDeserializer'
, 'RootAttributeSerializer'
, 'NodeAttributeDeserializer'
, 'NodeAttributeSerializer'
]
