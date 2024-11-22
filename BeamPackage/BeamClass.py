#!/usr/bin/env python
"""
Created on Tue Jul 16, 2024

@author: adukehart

NOTE: Need to think about determining the initial position of the beam and
locating the beam there at the beginning of the simulation.
"""

import numpy as np
from matplotlib.patches import Circle
from .Utilities import CircleRaster, XYRaster

class Beam:
    def __init__(self, size, position, R_circ, R_xy, omega_c, omega_xy):
        self.Time = 0
        self.size = size
        self.position = np.array(position)
        self.R_circ = R_circ
        self.R_xy = R_xy
        self.omega_c = omega_c
        self.omega_xy = np.array(omega_xy)
        
    def move(self, dt, frame):
        # Progress the dynamics forward by one step in time.
        self.position = (frame.get_center() 
                        + CircleRaster(self.Time, self.R_circ, self.omega_c)
                        + XYRaster(self.Time, self.R_xy, self.omega_xy)
                        )   
        self.Time += dt
        return self
    
    def render(self, ax):
        # This function is used to render the beam cross-section on the field
        # of view. Warning, this takes a lot of processing resources.
        circle = Circle(self.position, self.size/2, fc='blue', ec='black')
        ax.add_patch(circle)
        ax.set_aspect('equal')
        return ax