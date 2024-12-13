#!/usr/bin/env python
"""
Created on Fri Nov 22 14:21:02 2024

@author: adukehart
"""

import numpy as np

def Diameters(n):
    '''
    Generates an n-dimensional array of object diameters, where n is the number
    of objects. The diameters are randomly generated from a Gaussian
    distribuition. Diameters are reported in meters.

    Parameters
    ----------
    n : int
        The total number of objects being generated.

    Returns
    -------
    np.array
        An n-dimensional array of diameters.
    '''
    return np.random.normal(5.0, 1.0, n)/1000

def InitPositions(n, frame, fov):
    '''
    Generates an nx3 matrix of object initial positions, where n is the number
    of objects. The initial positions' x&y components are uniformly distributed
    between an arbitrary outer boundary and a 1000x1000 [meter] field of view, 
    while the z component is chosen from a Gaussian distribution. The
    coordinates of the initial positions are reported in meters.

    Parameters
    ----------
    n : int
        The total number of objects.
    frame : np.array
        A 2x2 matrix of x&y limits of the arbitrary outer frame.
    fov : np.array
        A 2x2 matrix of x&y limits of the field of view frame.

    Returns
    -------
    coord : np.array
        A nx3 array of positions. Each row in the matrix represents a set of
        coordiantes for one object.
    '''
    coord = np.empty((n, 3))
    for row in coord:
        while True:
            row[0] = np.random.uniform(frame[0][0], frame[0][1])
            row[1] = np.random.uniform(frame[1][0], frame[1][1])
            if not (fov[0][0] < row[0] < fov[0][1]):
                row[2] = np.random.normal(750.0, 150.0)*1000
                break
            if not (fov[1][0] < row[1] < fov[1][1]):
                row[2] = np.random.normal(750.0, 150.0)*1000
                break
    return coord
    
def Velocities(n, positions, fov):
    '''
    Generates an nx3 matrix of object velocities, where n is the number of
    objects. The z component of the velocity is 0, assuming there is no dift in
    the objects' altitude. The x&y components are randomly generated from a
    Gaussian distribution. The object velocities are reported in meters/second.

    Parameters
    ----------
    n : int
        The total number of objects.
    positions : np.array
        An nx3 array of initial positions.
    fov : np.array
        A 2x2 matrix of x&y limits of the field of view.

    Returns
    -------
    velocities : np.array
        A nx3 array of velocities. Each row in the matrix represents a velocity
        vector for one object.
    '''
    velocities = np.ones((n, 3))
    for i in range(0, n):
        velocities[i][:2] = np.random.normal(7650.0, 22.5)
        velocities[i][2] = 0.0
        point = np.random.uniform(fov[0][0], fov[0][1], 2)
        line = point - positions[i][:2]
        velocities[i][0] *= (line.dot(np.array([1, 0]))/np.sqrt(line.dot(line)))
        velocities[i][1] *= (line.dot(np.array([0, 1]))/np.sqrt(line.dot(line)))
    return velocities
