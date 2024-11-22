#!/usr/bin/env python
"""
Created on Wed Jul 17, 2024

@author: adukehart
"""

import numpy as np
import pylab as pl

class Object:
    def __init__(self, name, diameter, position, velocity, reflectance, altitude):
        self.id = name
        self.Time = 0
        self.diameter = diameter
        self.position = np.array(position)
        self.altitude = altitude
        self.velocity = np.array(velocity)
        self.reflectance = reflectance
        self.init_position = np.array(position)
        
        self.enter_flag = False
        self.exit_flag = False
        self.num_hits = 0
        
        self.patch = pl.Circle((self.position), self.diameter/2, 
                               fc='black', ec='black')
        
    def addHit(self):
        self.num_hits += 1
        
    def move(self, dt):
        if self.exit_flag != True:
            # Progress the dynamics forward by one time step.
            self.position = self.init_position + self.velocity * self.Time
            self.Time += dt
            return self
        else:
            return self
    
    def boundaryFlags(self, fov, delta):
        x_min = fov.M[0][0] - delta
        x_max = fov.M[0][1] + delta
        y_min = fov.M[1][0] - delta
        y_max = fov.M[1][1] + delta
        x_condition = x_min < self.position[0] < x_max
        y_condition = y_min < self.position[1] < y_max

        if x_condition == True and y_condition == True and self.enter_flag == False:
            self.enter_flag = True
        elif (x_condition == False or y_condition == False) and self.enter_flag == True:
            self.exit_flag = True
        return self
        
    def render(self, ax):
        # This function is used to render the object on the field of view.
        # Warning, this takes a lot of processing resources.
        circle = Circle(self.position, self.diameter/2, fc='black', ec='black')
        ax.add_patch(circle)
        ax.set_aspect('equal')
        return ax
    
    def printDetails(self):
        print(self.id)
        print(self.diameter)
        print(self.position)
        print(self.velocity)
        print(self.altitude)
        print(self.reflectance)
        print(self.num_hits)

###############################################################################
        
 
