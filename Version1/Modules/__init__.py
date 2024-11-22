#!/usr/bin/env python
"""
Created on Tue Jul 16, 2024

@author: adukehart
"""

# This code will be executed when the simulation package is imported
print("Loading Modules")

# Import specific functions and classes from the simulation modules
from .BeamClass import Beam
from .ObjectClass import Object, TrajectoryGenerator
from .FrameClass import Frame, BoundaryFlags
from .Collision import CollisionDetection

# Define the available classes and functions when using
# from DPAL_Simulation import *
__all__ = ['Beam', 'Object', 'TrajectoryGenerator', 'Frame', 'BoundaryFlags', 
           'CollisionDetection']

# Define version number
__version__ = '0.0.1'