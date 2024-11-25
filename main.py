#!/usr/bin/env python
"""
Created on Fri Nov 22 14:41:27 2024

@author: adukehart
"""

import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from BeamClass import Beam
from ObjectsClass import Objects
from ClockPackage import Clock

#SIMULATION PARAMETERS
time_step = 0.000001

# Define generating frame and field of view (fov)
frame = np.array([[-1500, 1500], [-1500, 1500]])
fov = np.array([[-500, 500], [-500, 500]])

# Initialize DPAL Beam
beam = Beam(Size = 2,
            R_circ = 304.88,
            R_xy = 195.12,
            ω_circ = 23230,
            ω_xy = np.array([2305, 990]))

# Initialize Simulation Clock
sim_clock = Clock()
sim_clock.reset()

# Initialize LEO Objects
obs = Objects(frame, fov, Num_Obs=10)

# Initialize DataFrame
headers = ['Simulation Time', 'Beam Location']
headers.extend(f"Object{i} Location" for i in range(obs.number))
data = []

times = []
while any(x == 0 for x in obs.enter_flags):
    start = time.time()
    
    # Update Component Positions
    beam.move(time_step, fov)
    obs.move(time_step)
    sim_clock.tick(time_step)
    
    # Update Object Flags
    obs.update_flags(fov, 2)
    
    # Record Position Data
    row = [sim_clock.Time, beam.get_position()]
    row.extend(obs.get_position(i) for i in range(obs.number))
    data.append(row)
    
    end = time.time()
    times.append(end-start)
    
position_data = pd.DataFrame(data=data, columns=headers)
position_data.to_csv("FasterTest.csv")
print("Total Simulation Time: ", sum(times))
plt.plot(range(len(times)), times)

    