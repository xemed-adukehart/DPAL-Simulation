# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 09:34:41 2024

@author: adukehart
"""

import numpy as np
import pandas as pd
from FramePackage import Frame, BoundaryFlags
from ObjectPackage import MultiObjectGenerator
from BeamPackage import Beam
from ClockPackage import Clock

time_step = 0.0001

# Set Frame configuration
frame = Frame(3000, 3000)                                   # UNITS: meters
fov = frame.make_fov(1/3)

# Set Default Beam Configuration
# NEED TO SET UP PUNCH CARD CONFIGURATION AND READ IN
beam_size = 2                                               # UNITS: meters
beam_init_position = fov.get_center()                       # UNITS: meters
circ_r = 304.88                                             # UNITS: meters
xy_r = 195.12                                               # UNITS: meters
circ_omega = 23230                                          # UNITS: Hz
xy_omega = [2305, 990]                                      # UNITS: Hz
beam = Beam(beam_size, 
               beam_init_position, 
               circ_r, 
               xy_r, 
               circ_omega, 
               xy_omega)

# Define objects vector
objects = MultiObjectGenerator(4, frame, fov)

# Initialize boundary flag vector
exit_flags = BoundaryFlags(objects, fov, 2)

# Initialize DataFrame
headers = ['Simulation Time', 'Beam Location']
for ob in objects:
    headers.append(f'{ob.id} Location')
df = pd.DataFrame(columns=headers)

# Initialize Simulation Timer
sim_time = Clock()
while (np.linalg.norm(exit_flags) != np.sqrt(len(exit_flags))):
    beam.move(time_step, fov)
    new_row = [sim_time.Time, beam.position]
    for ob in objects:
        ob.move(time_step)
        new_row.append(ob.position)
    
    df.loc[len(df)] = new_row
    sim_time.tick(time_step)
    exit_flags = BoundaryFlags(objects, fov, 2)
    
df.to_csv('test.csv')