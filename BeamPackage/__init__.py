# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 16:50:47 2024

@author: adukehart
"""

# This code will be executed when the simulation package is imported
print("Loading Beam Package")

# Import specific functions and classes from the simulation modules
from .Utilities import CircleRaster, XYRaster
from .BeamClass import Beam

# Define the available classes and functions when using
# from DPAL_Simulation import *
__all__ = ['Beam', 'CircleRaster', 'XYRaster']

# Define version number
__version__ = '0.0.1'