#!/usr/bin/env python
"""
Created on Fri Jul 19, 2024

@author: adukehart
"""

import numpy as np

def Detect(beam, objects):
    '''
    A check to see if the center of the object is within a beam radius of the
    center of the beam.

    Parameters
    ----------
    beam : Beam
        An instance of the Beam class.
    objects : Objects
        An instance of the Objects class.

    Returns
    -------
    np.array
        An array of bools where True means a collision between the beam and the
        ith object has been detected and False meaning no collision has been
        detected.

    '''
    object_list = []
    for row in objects.get_positions():
        vec = np.subtract(beam.get_position(), row[:2])
        if np.sqrt(vec.dot(vec)) < beam.size:
            object_list.append(True)
        else:
            object_list.append(False)
    return np.array(object_list)
