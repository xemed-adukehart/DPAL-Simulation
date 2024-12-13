#!/usr/bin/env python
"""
Created on Fri Nov 22 14:33:28 2024

@author: adukehart
"""

import numpy as np
from .Modules import  Raster

class Beam:
    def __init__(self, Size=0, R1=0, R2=0, ω1=0, ω2=0):
        self._time = 0
        self.size = Size
        self.r1 = R1
        self.r2 = R2
        self.ω1 = ω1
        self.ω2 = ω2
        self._position = np.zeros(2)

    @property
    def size(self) -> float:
        return self._size

    @property
    def r1(self) -> float:
        return self._r1

    @property
    def r2(self) -> float:
        return self._r2

    @property
    def ω1(self) -> float:
        return self._ω1

    @property 
    def ω2(self) -> np.array:
        return self._ω2

    @size.setter
    def size(self, value):
        if value < 0:
            raise ValueError("Size cannot be negative")
        self._size = value

    @r1.setter
    def r1(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._r1 = value
        
    @r2.setter
    def r2(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._r2 = value

    @ω1.setter
    def ω1(self, value):
        self._ω1 = value

    @ω2.setter
    def ω2(self, value):
        self._ω2 = value

    def get_position(self) -> np.array:
        return tuple(self._position)
    
    def reset(self):
        self._time = 0
        self._position = np.zeros(2)
        

    def move(self, dt, frame=None):
        if frame is None:
            self._position = Raster(self._time, self.r1, self.r2, self.ω1, self.ω2)
            self._time += dt
        else:
            self._position = ((frame[:][0] - frame[:][1])/2
                              + Raster(self._time, self.r1, self.r2, self.ω1, self.ω2))
            self._time += dt