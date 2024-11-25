#!/usr/bin/env python
"""
Created on Fri Jul 19, 2024

@author: adukehart
"""

import numpy as np

def CollisionDetection(beam, objects):
    '''
    Generates a hash map where the values are the number of collisions between
    the beam and and object

    Parameters
    ----------
    beam : TYPE
        DESCRIPTION.
    objects : TYPE
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.

    '''
    hits = {}
    for ob in objects:
        hits[ob] = 0
        
    beam_size = beam.size
    for ob in objects:
        ob_r = ob.diameter/2
    
        diff = ob.position[:1] - beam.position
        distance = np.sqrt(diff.dot(diff))
    
        if distance <= (ob_r + beam_size):
            hits[ob] += 1
    
    return hits