#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from cx_Freeze import setup, Executable

includes = ["os",
            "sys",
            "configparser",
            "argparse",
            "subprocess",
            "logzero"]

base = None

exe = Executable(script = './sasWrapperPy/sas.py',
                 base = base)

setup(name = 'sas',
      version = '0.1',
      author='Yui Tomo',
      license='MIT',
      description = 'Wrapper of SAS commands on Ubuntu on WSL',
      long_description=open('README.md').read(),
      executables = [exe])
