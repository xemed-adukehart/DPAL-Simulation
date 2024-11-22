#!usr/bin/env python
"""
Created on Wed Jul 17, 2024

@author: adukehart
"""

import numpy as np

class Frame:
    def __init__(self, dx, dy):
        self.M = np.array([[-dx/2, dx/2], 
                           [-dy/2, dy/2]])
        self.T = np.transpose(self.M)
        
    def get_center(self):
        '''
        Get the coordinates of the center of the frame.

        Returns
        -------
        center : ndarray
            A tuple that contains the x and y coordinates of the center of the 
            frame [x-center, y-center].
        '''
        center = (self.T[:][1] + self.T[:][0])/2
        return center
    
    def get_size(self):
        '''
        Get the length and width of the frame.

        Returns
        -------
        size : ndarray
            A tuple containing the x and y distances of the frame, i.e.
            [x-distance, y-distance].
        '''
        size = self.T[:][1] - self.T[:][0]
        return size
    
    def make_fov(self, p):
        '''
        Create a new frame by that is proportional to the old frame by a 
        factor p.
        
        Parameters
        ----------
        p : float
            The factor that changes the size of the frame for p < 1 the frame
            shrinks, for p > 1 the frame grows.

        Returns
        -------
        ndarray
            A new frame that is p-times the size of the original frame,
            centered at the same location.
        '''
        fov_size = p * self.get_size()
        return Frame(fov_size[0], fov_size[1])
    
    def get_axis(self): 
        xmin = self.M[0][0]
        xmax = self.M[0][1]
        ymin = self.M[1][0]
        ymax = self.M[1][1]
        return xmin, xmax, ymin, ymax
    
    def shift(self, dx, dy):
        new_frame = self
        for i in range(len(new_frame.M)):
            new_frame.M[0][i] += dx
            new_frame.M[1][i] += dy
        return new_frame
    
###############################################################################
