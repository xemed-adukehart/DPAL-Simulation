#!/usr/bin/env python
"""
Created on Fri Nov 22 14:21:02 2024

@author: adukehart
"""

import numpy as np

def IDs(n):
    return np.array(f"Object{i}" for i in range(n))

def Diameters(n):
    return np.random.normal(5.0, 1.0, n)/1000

def InitPositions(n, frame, fov):
    coord = np.empty((n, 3))
    for row in coord:
        while True:
            row[0] = np.random.uniform(frame[0][0], frame[0][1])
            row[1] = np.random.uniform(frame[1][0], frame[1][1])
            if not (fov[0][0] < row[0] < fov[0][1]):
                row[2] = np.random.normal(750.0, 150.0)*1000
                break
            elif not (fov[1][0] < row[1] < fov[1][1]):
                row[2] = np.random.normal(750.0, 150.0)*1000
                break
    return coord
    
def Velocities(n, positions, fov):
    velocities = np.ones((n, 3))
    for i in range(0, n):
        velocities[i][:2] = np.random.normal(7650.0, 22.5)
        velocities[i][2] = 0.0
        point = np.random.uniform(fov[0][0], fov[0][1], 2)
        line = point - positions[i][:2]
        velocities[i][0] *= (line.dot(np.array([1, 0]))/np.sqrt(line.dot(line)))
        velocities[i][1] *= (line.dot(np.array([0, 1]))/np.sqrt(line.dot(line)))
    return velocities