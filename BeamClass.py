#!/usr/bin/env python
"""
Created on Tue Jul 16, 2024

@author: adukehart

NOTE: Need to think about determining the initial position of the beam and
locating the beam there at the beginning of the simulation.
"""

import Modules.FrameClass                               # See FrameClass.py for details
import numpy as np
from math import cos, sin
from matplotlib.patches import Circle

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
                        + Circle_Raster(self.R_circ, self.omega_c, 0, self.Time)
                        + XY_Raster(self.R_xy, self.omega_xy, 0, self.Time)
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
    
###############################################################################

def Circle_Raster(R, omega, phi, t):
    '''
    Calculate the location of the circular raster at time t.

    Parameters
    ----------
    R : float
        The radius of the circular raster.
    omega : float
        The frequency of the circular raster.
    phi : float
        The phase of the circular raster, used to determine initial position.
    t : float
        The total time passed.

    Returns
    -------
    ndarray
        A tuple containing the x and y coordinates of the raster at time t 
        [x-coord, y-coord].
    '''
    x = R*cos(omega*t + phi)
    y = R*sin(omega*t + phi)
    return np.array([x, y])


def XY_Raster(R, omega, phi, t):
    '''
    Calculate the location of the xy-raster at time t.

    Parameters
    ----------
    R : float
        The radius of the raster.
    omega : ndarray
        A tuple containing the x and y frequencies of the raster 
        [x-freq, y-freq].
    phi : float
        The phase of the raster, used to determine initial position.
    t : float
        The total time passed.

    Returns
    -------
    ndarray
        A tuple contaning the x and y coordinates of the raster at time t
        [x-coord, y-coord].
    '''
    x = R*(0.8106*cos(omega[0]*t + phi) + 0.0901*cos(3*omega[0]*t + phi)
           + 0.0324*cos(5*omega[0]*t + phi) + 0.0165*cos(7*omega[0]*t + phi) 
           + 0.01*cos(9*omega[0]*t + phi) + 0.0067*cos(11*omega[0]*t + phi) 
           + 0.0048*cos(13*omega[0]*t + phi) + 0.0036*cos(15*omega[0]*t + phi) 
           + 0.0028*cos(17*omega[0]*t + phi) + 0.0022*cos(19*omega[0]*t + phi)
           )
    y = R*(0.8106*cos(omega[1]*t + phi) + 0.0901*cos(3*omega[1]*t + phi) 
           + 0.0324*cos(5*omega[1]*t + phi) + 0.0165*cos(7*omega[1]*t + phi) 
           + 0.01*cos(9*omega[1]*t + phi) + 0.0067*cos(11*omega[1]*t + phi) 
           + 0.0048*cos(13*omega[1]*t + phi) + 0.0036*cos(15*omega[1]*t + phi) 
           + 0.0028*cos(17*omega[1]*t + phi) + 0.0022*cos(19*omega[1]*t + phi)
           )
    return np.array([x, y])