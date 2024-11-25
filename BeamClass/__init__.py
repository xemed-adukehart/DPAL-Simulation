#!/usr/bin/env python
"""
Created on Fri Nov 22 14:36:34 2024

@author: adukehart
"""

# This code will be executed when the simulation package is imported
print("Loading Beam Package")

# Import specific functions and classes from the simulation module
from .Beam_cf import Beam

# Define the available classes and functions when using
# from DPAL_Simulation import *
__all__ = ['Beam']

# Define version number
__version__ = '0.0.1'