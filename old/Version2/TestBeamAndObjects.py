# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 09:42:59 2024

@author: adukehart
"""

import numpy as np
import pylab as pl
from FramePackage import Frame, BoundaryFlags
from BeamPackage import Beam
from ObjectPackage import MultiObjectGenerator
from Utils.Collision import CollisionDetection

pl.matplotlib.use('Qt5Agg')
#time_step = 0.00001

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
objects = MultiObjectGenerator(1, frame, fov)

# Initialize boundary flag vector
enter_flags = BoundaryFlags(objects, fov, 2, EntorEx=0)
exit_flags = BoundaryFlags(objects, fov, 2, EntorEx=1)

xmin, xmax, ymin, ymax = fov.get_axis()
fig = pl.figure()
ax = pl.axes(xlim=(xmin, xmax), ylim=(ymin,ymax))
ax.set_title('Field of View')

def Simulation(beam, objects, fov, enter_flags, exit_flags):
    while (np.linalg.norm(exit_flags) != np.sqrt(len(exit_flags))):
        while (np.linalg.norm(enter_flags) != 0):
            time_step = 0.000001
            pl.pause(0.001)
            beam.move(time_step, fov)
            beam_patch = pl.Circle((beam.position), beam.size/2, fc='blue',
                                   ec='blue')
            beam_patch.remove()
            ax.add_patch(beam_patch)
            for ob in objects:
                ob.move(time_step)
                object_patch = pl.Circle((ob.position), ob.diameter*50,
                                         fc='black', ec='black')
                ax.add_patch(object_patch)
                if CollisionDetection(beam, ob) == True:
                    ring_patch = pl.Circle((ob.position), 8, fc='None', ec='Yellow')
                    ax.add_patch(ring_patch)
        
            exit_flags = BoundaryFlags(objects, fov, 2, EntorEx=1)
        else:
            time_step = 0.001
            pl.pause(0.001)
            beam.move(time_step, fov)
            beam_patch = pl.Circle((beam.position), beam.size/2, fc='blue',
                                   ec='blue')
            ax.add_patch(beam_patch)
            for ob in objects:
                ob.move(time_step)
                object_patch = pl.Circle((ob.position), ob.diameter*50,
                                         fc='black', ec='black')
                ax.add_patch(object_patch) 
            
            enter_flags = BoundaryFlags(objects, fov, 2, EntorEx=0)
            exit_flags = BoundaryFlags(objects, fov, 2, EntorEx=1)

Simulation(beam, objects, fov, enter_flags, exit_flags)
pl.show()