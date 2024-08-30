#!/usr/bin/env python
"""
Created on Wed Jul 17, 2024

@author: adukehart
"""

import Modules.FrameClass                              # See FrameClass.py for details.
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, pi
from random import random, gauss, uniform
from matplotlib.patches import Circle

class Object:
    def __init__(self, diameter, position, velocity, reflectance, altitude):
        self.Time = 0
        self.diameter = diameter
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.reflectance = reflectance
        self.altitude = altitude
        self.init_position = np.array(position)
        
    def move(self, dt):
        # Progress the dynamics forward by one time step.
        self.position = self.init_position + self.velocity * self.Time
        self.Time += dt
        return self
    
    def render(self, ax):
        # This function is used to render the object on the field of view.
        # Warning, this takes a lot of processing resources.
        circle = Circle(self.position, self.diameter/2, fc='black', ec='black')
        ax.add_patch(circle)
        ax.set_aspect('equal')
        return ax

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
    return np.array([s*cos(theta), s*sin(theta), 0])


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


def TrajectoryGenerator(frame, fov, mean, std, altitude):
    '''
    Keep generating velocities so that the trajectory passes through the field 
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
    test_position = PositionGenerator(frame, fov, altitude)
    while True:
        test_velocity = VelocityGenerator(mean, std)
        if CheckTrajectory(test_position, test_velocity, frame, fov) == True:
            return test_position, test_velocity