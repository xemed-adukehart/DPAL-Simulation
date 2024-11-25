#!/usr/bin/env python
"""
Created on Fri Nov 22 14:35:38 2024

@author: adukehart
"""

import numpy as np

def CRaster(t, R, ω, ϕ=0):
    return np.array([R*np.cos(ω*t + ϕ),
                     R*np.sin(ω*t + ϕ)])
    
def func(t, R, ω, ϕ=0):
    return R*(0.8106*np.cos(ω*t + ϕ) + 0.0901*np.cos(3*ω*t + ϕ)
           + 0.0324*np.cos(5*ω*t + ϕ) + 0.0165*np.cos(7*ω*t + ϕ) 
           + 0.01*np.cos(9*ω*t + ϕ) + 0.0067*np.cos(11*ω*t + ϕ) 
           + 0.0048*np.cos(13*ω*t + ϕ) + 0.0036*np.cos(15*ω*t + ϕ) 
           + 0.0028*np.cos(17*ω*t + ϕ) + 0.0022*np.cos(19*ω*t + ϕ))
        
def XYRaster(t, R, ω, ϕ=0):
    return np.array([func(t, R, o, ϕ) for o in ω])