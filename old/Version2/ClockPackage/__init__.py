#!/usr/bin/env python
"""
Created on Tue Jul 16, 2024

@author: adukehart
"""

# This code will be executed when the simulation package is imported
print("Loading Simulation Clock")

# Import specific functions and classes from the simulation modules
from .ClockClass import Clock

# Define the available classes and functions when using
# from DPAL_Simulation import *
__all__ = ['Clock']

# Define version number
__version__ = '0.0.1'