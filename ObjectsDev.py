# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:12:44 2024

@author: adukehart
"""

import time
import numpy as np
import matplotlib.pyplot as plt

class Objects:
    def __init__(self, Frame, FOV, Num_Obs = 1):
        self.number = Num_Obs
        self._ids = IDs(Num_Obs)
        self._diameters = Diameters(Num_Obs)
        self._positions = InitPositions(Num_Obs, Frame, FOV)
        self._velocities = InitVelocities(Num_Obs, self._positions, FOV)
        self._reflectances = np.zeros(Num_Obs)
        self.enter_flags = np.zeros(Num_Obs)
        self.exit_flags = np.zeros(Num_Obs)
        self._dts = np.zeros((Num_Obs,1))

    def move(self, dt):
        for i in range(0, self.number):
            self._positions[i] += self._velocities[i]*dt

    def update_flags(self, fov, delta):
        x_min = fov[0][0] - delta
        x_max = fov[0][1] + delta
        y_min = fov[1][0] - delta
        y_max = fov[1][1] + delta
        for i in range(len(self._positions)):
            x_cond = x_min < self._positions[i][0] < x_max
            y_cond = y_min < self._positions[i][1] < y_max
            if x_cond == True and y_cond == True and self.enter_flags[i] == 0:
                self.enter_flags[i] = 1
            elif (x_cond == False or y_cond == False) and self.enter_flags[i] == 1:
                self.exit_flags[i] = 1
                
    def get_ids(self):
        return self._ids
        
    def get_positions(self):
        return self._positions
    
    def get_velocities(self):
        return self._velocities
    
def IDs(n):
    return np.array(f"Object{i}" for i in range(0, n))

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
    
def InitVelocities(n, positions, fov):
    velocities = np.ones((n, 3))
    for i in range(0, n):
        velocities[i][:2] = np.random.normal(7650.0, 22.5)
        velocities[i][2] = 0.0
        point = np.random.uniform(fov[0][0], fov[0][1], 2)
        line = point - positions[i][:2]
        velocities[i][0] *= (line.dot(np.array([1, 0]))/np.sqrt(line.dot(line)))
        velocities[i][1] *= (line.dot(np.array([0, 1]))/np.sqrt(line.dot(line)))
    return velocities

frame = np.array([[-1500, 1500],[-1500, 1500]])
fov = np.array([[-500, 500],[-500, 500]])
obs = Objects(frame, fov, 10)

times = []
t = 0
while any(x == 0 for x in obs.exit_flags):
    start = time.time()
    obs.move(0.000001)
    obs.update_flags(fov, 2)
    end = time.time()
    times.append(end-start)
plt.plot(range(0, len(times)), times)
print(sum(elem for elem in times))
print(obs.enter_flags)
print(obs.exit_flags)
print(obs.get_positions())