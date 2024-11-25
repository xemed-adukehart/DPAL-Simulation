# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 09:51:45 2024

@author: adukehart
"""

import numpy as np
from random import uniform, gauss, random;
from math import pi
from .Utilities import CheckTrajectory
from .ObjectClass import Object

def PositionGenerator(frame, fov, altitude):
    '''
    Generate a random 3D position vector with fixed Z-component. A uniform 
    distribution of points that fall between the edge of the frame and the 
    field of view.

    Parameters
    ----------
    frame : ndarray
        A 2x2 matrix containing the bounding values for where objects can be
        generated.
    fov : ndarray
        A 2x2 matrix containing the bounding values for area that is visible to 
        the detector.
   altitude : float
       The altitude of the object above the ground.

    Returns
    -------
    ndarray
        A random position vector with fixed altitude.
    '''
    while True:
        X = uniform(frame.M[0][0], frame.M[0][1])
        Y = uniform(frame.M[1][0], frame.M[1][1])
        if not (fov.M[0][0] < X < fov.M[0][1]):
            return np.array([X, Y, altitude])
        elif not (fov.M[1][0] < Y < fov.M[1][1]):
            return np.array([X, Y, altitude])
        
###############################################################################

def AltitudeGenerator():
    '''
    Generate a random altitude. Probability distribution taken from:
    https://www.hdi.global/globalassets/_local/international/newsroom/hdi_global_specialty_study_space_debris_2023_corpv5.pdf

    Returns
    -------
    float
        An altitude.
    '''
    a = gauss(750.0, 150.0)                       # mean: 750 km, sigma: 150 km
    return a*1000                                # return an altitude in meters

###############################################################################

def SizeGenerator():
    '''
    Generates a random diameter between 3.5mm and 10cm

    Returns
    -------
    float
        A diameter
    '''
    s = gauss(5.0, 1.0)
    return s/100

###############################################################################

def VelocityGenerator(mean, std):
    '''
    Generate a random 3D velocity vector with no Z-directional components.

    Parameters
    ----------
    mean : float
        The mean of the Gaussian dist. used to generate random magnitudes.
    std : float
        The standard deviation of the Gaussian dist. used to generate random
        magnitudes.

    Returns
    -------
    ndarray
        A velocity vector with no movement in the Z-direction.
    '''
    theta = 2*pi*random()
    s = gauss(mean, std)
    return np.array([s*np.cos(theta), s*np.sin(theta), 0])

###############################################################################

def TrajectoryGenerator(frame, fov, altitude, mean=7650, std=22.5):
    '''
    Keep generating velocities until the trajectory passes through the field 
    of view.

    Parameters
    ----------
    frame : ndarray
        A 2x2 matrix containing the bounding values for where objects can be
        generated.
    fov : ndarray
        A 2x2 matrix containing the bounding values for area that is visible to 
        the detector.
    mean : float
        The mean of the Gaussian dist. used to generate velocity.
    std : float
        The standard deviation of the Gaussian dist. used to generate velocity.
    altitude : float
        The altitude of the object above the ground.

    Returns
    -------
    test_position : ndarray
        A randomly generated position that forms a trajectory which passes
        through the field of view.
    test_velocity : ndarray
        A randomly generated velocity that forms a trajectory which passes
        through the field of view.
    '''
    position = PositionGenerator(frame, fov, altitude)

    while True:
        test_velocity = VelocityGenerator(mean, std)
        if CheckTrajectory(position, test_velocity, frame, fov) == True:
            return position, test_velocity
        
        
def MultiObjectGenerator(num_obs, frame, fov):
    '''
    Generate n Object Class objects with unique properties.

    Parameters
    ----------
    num_obs : int
        The total number of objects generated.
    frame : Frame
        The Frame being used to simulate object trajectories.
    fov : Frame
        The field of view.

    Returns
    -------
    ob_list : Array
        An array of Object Class elements.

    '''
    ob_list = []
    for i in range(num_obs):
        name = f"object{i}"
        diameter = SizeGenerator()                               # in meters
        reflectance = 1                                         # unknown units
        altitude = AltitudeGenerator()                           # in meters
        init_position, velocity = TrajectoryGenerator(frame, fov, altitude)
        ob = Object(name, diameter, init_position, velocity, reflectance, 
                       altitude)
        ob_list.append(ob)
    
    return ob_list