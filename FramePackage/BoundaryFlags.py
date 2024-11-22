# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 16:39:01 2024

@author: adukehart
"""

import numpy as np

def BoundaryFlags(objects, fov, delta, EntorEx=0):
    x_min = fov.M[0][0] - delta
    x_max = fov.M[0][1] + delta
    y_min = fov.M[1][0] - delta
    y_max = fov.M[1][1] + delta
    
    enter_list = np.zeros(len(objects))
    exit_list = np.zeros(len(objects))
    
    for ob in objects:
        x_con = x_min < ob.position[0] < x_max
        y_con = y_min < ob.position[1] < y_max
    
        if x_con == True and y_con == True and ob.enter_flag == False:
            ob.enter_flag = True
            enter_list[objects.index(ob)] = 1
        elif (x_con == False or y_con == False) and ob.enter_flag == True:
            ob.exit_flag = True
            exit_list[objects.index(ob)] = 1
    if EntorEx == 0:
        return enter_list
    else:
        return exit_list