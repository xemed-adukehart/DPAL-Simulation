# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 08:34:08 2024

@author: adukehart
"""

import numpy as np
import pylab as pl
from FramePackage import Frame, BoundaryFlags
from ObjectPackage import MultiObjectGenerator

pl.matplotlib.use('Qt5Agg')

time_step = 0.001

# Define frame and field of view
frame = Frame(3000, 3000)
fov = frame.make_fov(1/3)

# Define objects vector
objects = MultiObjectGenerator(4, frame, fov)

# Initialize boundary flag vector
exit_flags = BoundaryFlags(objects, fov, 2)

xmin, xmax, ymin, ymax = fov.get_axis()
fig = pl.figure()
ax = pl.axes(xlim=(xmin, xmax), ylim=(ymin,ymax))
ax.tick_params(axis='both', which='both',
               bottom=False,
               left=False,
               labelbottom=False,
               labelleft=False)
ax.set_title('Field of View')

while (np.linalg.norm(exit_flags) != np.sqrt(len(exit_flags))):
    pl.pause(0.001)
    for ob in objects:
        ob.move(time_step)
        patch = pl.Circle((ob.position), ob.diameter/2,
                          fc='black', ec='black')
        ax.add_patch(patch)
        
    exit_flags = BoundaryFlags(objects, fov, 2)

pl.show()