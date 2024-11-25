# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 16:40:37 2024

@author: adukehart
"""

# This code will be executed when the simulation package is imported
print("Loading Frame Modules")

# Import specific functions and classes from the simulation modules
from .FrameClass import Frame
from .BoundaryFlags import BoundaryFlags

# Define the available classes and functions when using
# from DPAL_Simulation import *
__all__ = ['Frame', 'BoundaryFlags']

# Define version number
__version__ = '0.0.1'