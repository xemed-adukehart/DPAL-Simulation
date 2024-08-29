#!/usr/bin/env python
"""
Created on Fri Jul 19, 2024

@author: adukehart
"""

import Modules.BeamClass
import Modules.ObjectClass
import numpy as np

def CollisionDetection(beam, objecta):
    ob_r = objecta.diameter/2
    beam_size = beam.size
    
    diff = objecta.position[:1] - beam.position
    distance = np.sqrt(diff.dot(diff))
    
    if distance <= (ob_r + beam_size):
        return True
    else:
        return False