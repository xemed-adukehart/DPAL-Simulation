# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 09:31:15 2024

@author: adukehart
"""

import numpy as np

def CircleRaster(t, R, omega, phi=0):
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
    x = R*np.cos(omega*t + phi)
    y = R*np.sin(omega*t + phi)
    return np.array([x, y])

def XYRaster(t, R, omega, phi=0):
    '''
    Calculate the location of the xy-raster at time t.

    Parameters
    ----------
    R : float
        The radius of the raster.
    omega : ndarray
        A tuple containing the x and y frequencies of the raster 
        [x-freq, y-freq].
    phi : float (optional)
        The phase of the raster, used to determine initial position.
    t : float
        The total time passed.

    Returns
    -------
    ndarray
        A tuple contaning the x and y coordinates of the raster at time t
        [x-coord, y-coord].
    '''
    x = R*(0.8106*np.cos(omega[0]*t + phi) + 0.0901*np.cos(3*omega[0]*t + phi)
           + 0.0324*np.cos(5*omega[0]*t + phi) + 0.0165*np.cos(7*omega[0]*t + phi) 
           + 0.01*np.cos(9*omega[0]*t + phi) + 0.0067*np.cos(11*omega[0]*t + phi) 
           + 0.0048*np.cos(13*omega[0]*t + phi) + 0.0036*np.cos(15*omega[0]*t + phi) 
           + 0.0028*np.cos(17*omega[0]*t + phi) + 0.0022*np.cos(19*omega[0]*t + phi)
           )
    y = R*(0.8106*np.cos(omega[1]*t + phi) + 0.0901*np.cos(3*omega[1]*t + phi) 
           + 0.0324*np.cos(5*omega[1]*t + phi) + 0.0165*np.cos(7*omega[1]*t + phi) 
           + 0.01*np.cos(9*omega[1]*t + phi) + 0.0067*np.cos(11*omega[1]*t + phi) 
           + 0.0048*np.cos(13*omega[1]*t + phi) + 0.0036*np.cos(15*omega[1]*t + phi) 
           + 0.0028*np.cos(17*omega[1]*t + phi) + 0.0022*np.cos(19*omega[1]*t + phi)
           )
    return np.array([x, y])