#!/usr/bin/env python
"""
Created on Fri Nov 22 13:53:16 2024

@author: adukehart
"""

import numpy as np
from .Modules import Diameters, InitPositions, Velocities

class Objects:
    def __init__(self, Frame, FOV, Num_Obs = 1):
        self.number = Num_Obs
        self.diameters = Diameters(Num_Obs)
        self._positions = InitPositions(Num_Obs, Frame, FOV)
        self._velocities = Velocities(Num_Obs, self._positions, FOV)
        self._reflectances = np.zeros(Num_Obs)
        self.enter_flags = np.zeros(Num_Obs)
        self.exit_flags = np.zeros(Num_Obs)

    def move(self, dt):
        '''
        This method updates the position matrix according to the objects' 
        motion. Currently, only simple linear motion is assumed.

        Parameters
        ----------
        dt : float
            The time step.

        Returns
        -------
        None.
        '''
        for i in range(0, self.number):
            self._positions[i] += self._velocities[i]*dt

    def update_flags(self, frame, delta):
        '''
        Updates the vectors that signal whether or not an object is within the
        field of view using 0 and 1 as bool values (0 -> False, 1 -> True). The
        enter flag signals when an object has entered a desired frame for the
        first time, and the exit flag signals when an object has left the
        frame, after entering.

        Parameters
        ----------
        fov : np.array
            A 2x2 matrix of x&y limits of the field of view frame.
        delta : float
            An offset that allows the objects position to exceed the frame if 
            needed.

        Returns
        -------
        None.

        '''
        x_min = frame[0][0] - delta
        x_max = frame[0][1] + delta
        y_min = frame[1][0] - delta
        y_max = frame[1][1] + delta
        for i in range(len(self._positions)):
            x_cond = x_min < self._positions[i][0] < x_max
            y_cond = y_min < self._positions[i][1] < y_max
            if x_cond == True and y_cond == True and self.enter_flags[i] == 0:
                self.enter_flags[i] = 1
            elif (x_cond == False or y_cond == False) and self.enter_flags[i] == 1:
                self.exit_flags[i] = 1
                
    # Getter methods
    def get_position(self, n):
        return tuple(self._positions[n])
    
    def get_positions(self):
        return tuple(map(tuple, self._positions))
    
    def get_altitude(self, n):
        return float(self._positions[n][2])
    