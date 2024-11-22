# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:06:44 2024

@author: adukehart
"""

import numpy as np

def CheckTrajectory(position, velocity, frame, fov):
    '''
    Check to make sure the randomly generated position/velocity will form a 
    trajectory that passes through the field of view.

    Parameters
    ----------
    position : ndarray
        Numpy array that represents the position of an object at fixed altitude.
    velocity : ndarray
        Numpy array that represents the 2D velocity of an object.
    frame : ndarray
        A 2x2 matrix containing the bounding values for where objects can be
        generated.
    fov : ndarray
        A 2x2 matrix containing the bounding values for area that is visible to 
        the detector.

    Returns
    -------
    bool
        TRUE if the trajectory pass through the fov, FALSE otherwise.
    '''
    size = frame.get_size()
    t_max = np.sqrt(size.dot(size)) / np.sqrt(velocity.dot(velocity))
    
    for t in np.arange(0, t_max, 0.1):
        if ((fov.M[0][0] < position[0] + velocity[0]*t < fov.M[0][1]) 
            and (fov.M[1][0] < position[1] + velocity[1]*t < fov.M[1][1])):
                return True
    return False

def MoveObjects(ob_list, time_step, record=None):
    if record is not None:
        for ob in ob_list:
            ob.move(time_step)
            record.append(ob.position)
        return ob_list, record
    else:
        for ob in ob_list:
            ob.move(time_step)
        return ob_list