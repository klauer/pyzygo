#!/usr/bin/env python

"""
Python to zygo interferometer (mrc3 / MetroPro)

> python setup.py build
> python setup.py install
"""

from distutils.core import setup, Extension
from sys import version_info

import os

callback_dll = Extension('_mrc3_callbacks',
                         sources=['callback_fix.c'],
                         libraries=['mrc3_client'],
                         language='c++',)

setup(name='mrc4',
      version='0.1',
      author="Ken Lauer",
      description="""Host automation products interface through Python""",
      ext_modules=[callback_dll],
      py_modules=[],
      )

import os
os.system(r'copy build\lib.win32-%d.%d\*.pyd .' % (version_info[:2]))
