#!/usr/bin/env python
"""
Created on Fri Nov 22 14:25:54 2024

@author: adukehart
"""

# Import specific functions and classes from the simulation module
from .Objects_cf import Objects

# This code will be executed when the simulation package is imported
print("Loading Object Package")

# Define the available classes and functions when using
# from DPAL_Simulation import *
__all__ = ['Objects']

# Define version number
__version__ = '0.0.1'
