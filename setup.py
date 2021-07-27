#!/usr/bin/env python
from distutils.core import setup,Extension
import sys

setup(
  name='FitAllB',
  version='1.1.1',
  description='Fitting routines for global parameters (fitgloball), global parameters for each grain (fitglobalgrain) and grain cms, orientations and strain (fitallb)',
  license='GPL', maintainer='Jette Oddershede',
  maintainer_email='jeto@fysik.dtu.dk',
  url='https://github.com/jadball/FitAllB',
  packages=["FitAllB"],
  package_dir={"FitAllB":"FitAllB"},
  scripts=["scripts/fitallb.py","scripts/fitgloball.py","scripts/fitglobalgrain.py","scripts/fitgloball_multidet.py"]
)
