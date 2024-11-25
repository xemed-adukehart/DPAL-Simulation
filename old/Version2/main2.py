# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 14:26:06 2024

@author: adukehart
"""

# Import Necessary Packages
import gc
import time
import numpy as np
import pandas as pd
import random as rand
import matplotlib.pyplot as plt

from BeamPackage import Beam
from ClockPackage import Clock
from FramePackage import Frame, BoundaryFlags
from ObjectPackage import MultiObjectGenerator, MoveObjects
from Utils.Collision import CollisionDetection
from Utils.datetime_utils import formatDate, getCurrentDate

rand.seed(10)   # For consistency, not necessary

def main():
    # SIMULATION PARAMETERS
    run_num = 1                                          # Fixed, DO NOT CHANGE
    total_runs = 1                                        # Adjustable argument
    
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
    beam = Beam(beam_size, beam_init_position, circ_r, xy_r, circ_omega, 
                   xy_omega)
    
    # Set Simulation clock
    clock = Clock()
    
    # Start the wall clock
    main_timer_start = time.perf_counter()
    
    loop_times = []
    
    # MAIN SIMULATION
    while run_num < total_runs+1:
        # Set Object Configuration
        objects = MultiObjectGenerator(3, frame, fov)
        
        # Initialize boundary flag vector
        enter_flags = BoundaryFlags(objects, fov, 2, EntorEx=0)
        exit_flags = BoundaryFlags(objects, fov, 2, EntorEx=1)
        
        # Initialize DataFrame
        headers = ['Simulation Time', 'Beam Location']
        for ob in objects:
            headers.append(f'{ob.id} Location')
        df = pd.DataFrame(columns=headers)
        
        print(f"Starting Run {run_num}")
        
        while (np.linalg.norm(enter_flags) == 0):
            time_step = 0.001
            
            beam.move(time_step, fov)
            objects = MoveObjects(objects, time_step)
            clock.tick(time_step)
            
            enter_flags = BoundaryFlags(objects, fov, 2, EntorEx=0)
            exit_flags = BoundaryFlags(objects, fov, 2, EntorEx=1)
        
        while (np.linalg.norm(exit_flags) != np.sqrt(len(exit_flags))):
            start = time.time()
            time_step = 0.000001
            
            beam.move(time_step, fov)
            row = [clock.Time, beam.position]
            objects, row = MoveObjects(objects, time_step, record=row)
            clock.tick(time_step)
            
            df.loc[len(df)] = row
            exit_flags = BoundaryFlags(objects, fov, 2, EntorEx=1)
            end = time.time()
            gc.collect()
            loop_times.append(end-start)
            
        run_num +=1
    plt.plot(range(0, len(loop_times)), loop_times)
    plt.show()    
    elapsed_main_time = round((time.perf_counter() - main_timer_start), 2) 
    print(elapsed_main_time)
        
if __name__=="__main__":
    main()