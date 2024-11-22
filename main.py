#!/usr/bin/env python
"""
Created on Fri Aug 30 15:52:57 2024

@author: adukehart
"""

# Import Necessary Packages
import time
import numpy as np
import pandas as pd
import random as rand

from BeamPackage import Beam
from ClockPackage import Clock
from FramePackage import Frame, BoundaryFlags
from ObjectPackage import MultiObjectGenerator, MoveObjects
from Utils.Collision import CollisionDetection
from Utils.datetime_utils import formatDate, getCurrentDate

rand.seed(10)   # For consistency, not necessary

def main():
    # Create Results output file
    date = formatDate(getCurrentDate())
    results_file_name = date + "Results.txt"
    results_file = open(results_file_name, 'a')
    
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
    
    # Write beam configuration to Results.txt
    '''
    results_file.write(f"RESULTS FOR {date} SIMULATION")
    results_file.write("\n")
    results_file.write("\n** BEAM PROPERTIES **")
    results_file.write(f"\n    -- Beam Width:                          {beam_size} m")
    results_file.write(f"\n    -- Beam Starting Position:              [{round(beam_init_position[0],2)}, {round(beam_init_position[1],2)}] m")
    results_file.write(f"\n    -- Circular Raster Radius:              {circ_r} m")
    results_file.write(f"\n    -- XY Raster Radius:                    {xy_r} m")
    results_file.write(f"\n    -- Circular Raster Angular Velocity:    {circ_omega} Hz")
    results_file.write(f"\n    -- XY Raster Angular Velocity:          {xy_omega} Hz")
    '''
    clock = Clock()

    # MAIN SIMULAITON
    print(f"Starting Simulation: {total_runs} runs")
    main_timer_start = time.perf_counter()
    
    while run_num < total_runs+1:
        # Set up parameters and detection data
        clock.reset()
        
        results_file.write("\n")
        results_file.write("\n--------------------------------------------------------------")
        results_file.write(f"\nStarting Run {run_num}")
        
        # Set Object Configuration
        objects = MultiObjectGenerator(3, frame, fov)
        
        hits = {}
        for ob in objects:
            hits[ob] = 0
        
        # Initialize boundary flag vector
        enter_flags = BoundaryFlags(objects, fov, 2, EntorEx=0)
        exit_flags = BoundaryFlags(objects, fov, 2, EntorEx=1)
        
        run_timer_start = time.perf_counter()
        
        # Initialize DataFrame
        headers = ['Simulation Time', 'Beam Location']
        for ob in objects:
            headers.append(f'{ob.id} Location')
        df = pd.DataFrame(columns=headers)
        
        print(f"Starting Run {run_num}")
       
        while (np.linalg.norm(exit_flags) != np.sqrt(len(exit_flags))):
            while (np.linalg.norm(enter_flags) == 0):
                time_step = 0.001
                beam.move(time_step, fov)
                objects = MoveObjects(objects, time_step)
                clock.tick(time_step)
                
                enter_flags = BoundaryFlags(objects, fov, 2, EntorEx=0)
                exit_flags = BoundaryFlags(objects, fov, 2, EntorEx=1)
                 
            time_step = 0.000001
                
            beam.move(time_step, fov)
            row = [clock.Time, beam.position]

            objects, row = MoveObjects(objects, time_step, record=row)
            clock.tick(time_step)
                
            if CollisionDetection(beam, ob) == True:
                new_fov = fov.shift(ob.position[0], ob.position[1])
                new_flags = BoundaryFlags(objects, new_fov, 2, EntorEx=1)
                

                break
                
            df.loc[len(df)] = row
            exit_flags = BoundaryFlags(objects, fov, 2, EntorEx=1)
                

        # Process Run results
        elapsed_run_time = round((time.perf_counter() - run_timer_start), 3)
        
        results_file.write("\n")
        results_file.write("\n** RUN RESULTS **")
        results_file.write(f"\n    -- Run Time:                 {elapsed_run_time}")
        for ob in objects:
            results_file.write(f"\n    -- {ob.id} Detections:     {ob.num_hits}")
        
        df.to_csv(date + f' Run {run_num} of {total_runs} Data.csv')
        
        print(f"Ending run {run_num} of {total_runs}")
        run_num += 1
    
    print("Ending Simulation")
    
    elapsed_main_time = round((time.perf_counter() - main_timer_start), 2)    
    
    results_file.write("\n")
    results_file.write("\n------------------------------------------------------------------")
    results_file.write("\n** FINAL RESULTS **")
    results_file.write(f"\nSimulation Time:    {elapsed_main_time} s")
    # print(f"Memory Usage:       {memMb} MB")
    results_file.close()
        
if __name__=="__main__":
    main()