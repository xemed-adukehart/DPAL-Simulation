#!/usr/bin/env python
"""
Created on Tue Oct  1 15:05:00 2024

@author: adukehart
"""

# This code will be executed when the simulation package is imported
print("Loading Object Package")

# Import specific functions and classes from the simulation modules
from .Generators import (PositionGenerator, AltitudeGenerator, SizeGenerator,
                         VelocityGenerator, TrajectoryGenerator,
                         MultiObjectGenerator)
from .Utilities import CheckTrajectory, MoveObjects
from .ObjectClass import Object

# Define the available classes and functions when using
# from DPAL_Simulation import *
__all__ = ['PositionGenerator', 'AltitudeGenerator', 'SizeGenerator',
           'VelocityGenerator', 'TrajectoryGenerator', 
           'CheckTrajectory', 'MultiObjectGenerator', 'MoveObjects', 'Object']

# Define version number
__version__ = '0.0.1'