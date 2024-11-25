#!/usr/bin/env python
"""
Created on Fri Nov 22 14:33:28 2024

@author: adukehart
"""

import numpy as np
from .Modules import CRaster, XYRaster

class Beam:
    def __init__(self, Size=0, R_circ=0, R_xy=0, ω_circ=0, ω_xy=np.zeros(2)):
        self._time = 0
        self.size = Size
        self.r_circ = R_circ
        self.r_xy = R_xy
        self.ω_circ = ω_circ
        self.ω_xy = ω_xy
        self._position = np.zeros(2)

    @property
    def size(self) -> float:
        return self._size

    @property
    def r_circ(self) -> float:
        return self._r_circ

    @property
    def r_xy(self) -> float:
        return self._r_xy

    @property
    def ω_circ(self) -> float:
        return self._ω_circ

    @property 
    def ω_xy(self) -> np.array:
        return self._ω_xy

    @size.setter
    def size(self, value):
        if value < 0:
            raise ValueError("Size cannot be negative")
        self._size = value

    @r_circ.setter
    def r_circ(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._r_circ = value
        
    @r_xy.setter
    def r_xy(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._r_xy = value

    @ω_circ.setter
    def ω_circ(self, value):
        self._ω_circ = value

    @ω_xy.setter
    def ω_xy(self, value):
        if value.size != 2:
            raise ValueError("Parameter must be a vector of length 2")
        self._ω_xy = value

    def get_position(self) -> np.array:
        return tuple(self._position)

    def move(self, dt, frame=None):
        if frame is None:
            self._position = (CRaster(self._time, self.r_circ, self.ω_circ)
                              + XYRaster(self._time, self.r_xy, self.ω_xy))
            self._time += dt
        else:
            self._position = ((frame[:][0] + frame[:][1])/2
                              + CRaster(self._time, self.r_circ, self.ω_circ)
                              + XYRaster(self._time, self.r_xy, self.ω_xy))
            self._time += dt