#!/usr/bin/env python
"""
Created on Fri Nov 22 14:35:38 2024

@author: adukehart
"""

import numpy as np

#def CRaster(t, R, ω, ϕ=0):
#    return np.array([R*np.cos(ω*t + ϕ),
#                     R*np.sin(ω*t + ϕ)])
    
#def func(t, R, ω, ϕ=0):
#    return R*(0.8106*np.cos(ω*t + ϕ) + 0.0901*np.cos(3*ω*t + ϕ)
#           + 0.0324*np.cos(5*ω*t + ϕ) + 0.0165*np.cos(7*ω*t + ϕ) 
#           + 0.01*np.cos(9*ω*t + ϕ) + 0.0067*np.cos(11*ω*t + ϕ) 
#           + 0.0048*np.cos(13*ω*t + ϕ) + 0.0036*np.cos(15*ω*t + ϕ) 
#           + 0.0028*np.cos(17*ω*t + ϕ) + 0.0022*np.cos(19*ω*t + ϕ))
        
#def XYRaster(t, R, ω, ϕ=0):
#    return np.array([func(t, R, o, ϕ) for o in ω])

def Raster(t, R1, R2, ω1, ω2, ϕ1=0, ϕ2=0):
    '''
    Determines the xy-coordinate position of the tip of the DPAL beam at an
    absolute time t. The motion of the raster is spirographic. The first radius
    R1 determines the average radius of the circles mapped out by the beam tip
    and R2 determines the "thickness" of the annulus mapped out by the beam tip.

    Parameters
    ----------
    t : float
        Absolute time.
    R1 : float
        The radius of the first circular raster.
    R2 : float
        The radius of the second circular raster.
    ω1 : float
        The frequency of the first circular raster.
    ω2 : float
        The frequency of the second circular raster.
    ϕ1 : float, optional
        The phase of the first circular rster. The default is 0.
    ϕ2 : float, optional
        The phase of the second circular raster. The default is 0.

    Returns
    -------
    np.arrray
        The xy-coordiate position of the tip of the DPAL beam.

    '''
    return np.array([R1*np.cos(ω1*t + ϕ1) + R2*np.cos(ω2*t + ϕ2),
                     R1*np.sin(ω1*t + ϕ1) + R2*np.sin(ω2*t + ϕ2)])