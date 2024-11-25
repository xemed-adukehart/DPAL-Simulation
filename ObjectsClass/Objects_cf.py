#!/usr/bin/env python
"""
Created on Fri Nov 22 13:53:16 2024

@author: adukehart
"""

import numpy as np
from .Modules import IDs, Diameters, InitPositions, Velocities

class Objects:
    def __init__(self, Frame, FOV, Num_Obs = 1):
        self.number = Num_Obs
        self._ids = IDs(Num_Obs)
        self.diameters = Diameters(Num_Obs)
        self._positions = InitPositions(Num_Obs, Frame, FOV)
        self._velocities = Velocities(Num_Obs, self._positions, FOV)
        self._reflectances = np.zeros(Num_Obs)
        self.enter_flags = np.zeros(Num_Obs)
        self.exit_flags = np.zeros(Num_Obs)

    def move(self, dt):
        for i in range(0, self.number):
            self._positions[i] += self._velocities[i]*dt

    def update_flags(self, fov, delta):
        x_min = fov[0][0] - delta
        x_max = fov[0][1] + delta
        y_min = fov[1][0] - delta
        y_max = fov[1][1] + delta
        for i in range(len(self._positions)):
            x_cond = x_min < self._positions[i][0] < x_max
            y_cond = y_min < self._positions[i][1] < y_max
            if x_cond == True and y_cond == True and self.enter_flags[i] == 0:
                self.enter_flags[i] = 1
            elif (x_cond == False or y_cond == False) and self.enter_flags[i] == 1:
                self.exit_flags[i] = 1
    
    def get_id(self, n):
        return self._ids[n]
        
    def get_position(self, n):
        return tuple(self._positions[n])