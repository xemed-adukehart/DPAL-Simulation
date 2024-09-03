#!/usr/bin/env python
"""
Created on Fri Aug 30 15:52:57 2024

@author: adukehart
"""

# Import Necessary Packages
import time
import argparse
import Modules.FrameClass as fc
import Modules.BeamClass as bc
import Modules.ObjectClass as oc
import random as rand
from Utils.file_utils import readFile, writeFile
from Utils.datetime_utils import formatDate, getCurrentDate
from Modules.Collision import CollisionDetection

rand.seed(10)   # For consistency, not necessary

def main():
    # A test of argument parser feature
    parser = argparse.ArgumentParser(description='Run a DPAL Simulation')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    
    # Create Results output file
    date = formatDate(getCurrentDate())
    results_file_name = date + "Results.txt"
    results_file = open(results_file_name, 'a')
    
    # Create Location Data output file
    location_file_name = date + "Location_Data.log"
    location_file = open(location_file_name, 'a')
    location_file.write("# Time, Beam Location, Object Location")
    
    # SIMULATION PARAMETERS
    run_num = 1                                          # Fixed, DO NOT CHANGE
    results = {}                                         # Fixed, DO NOT CHANGE
    time_step = 0.000001            # Adjustable argument, in seconds
    total_runs = 1                  # Adjustable argument
    
    # Set Frame configuration
    frame = fc.Frame(3000, 3000)                                # UNITS: meters
    fov = frame.make_fov(1/3)
    
    # Set Default Beam Configuration
    # NEED TO SET UP PUNCH CARD CONFIGURATION AND READ IN
    beam_size = 2                                               # UNITS: meters
    beam_init_position = fov.get_center()                       # UNITS: meters
    circ_r = 304.88                                             # UNITS: meters
    xy_r = 195.12                                               # UNITS: meters
    circ_omega = 23230                                          # UNITS: Hz
    xy_omega = [2305, 990]                                      # UNITS: Hz
    beam = bc.Beam(beam_size, 
                   beam_init_position, 
                   circ_r, 
                   xy_r, 
                   circ_omega, 
                   xy_omega)
    # Write beam configuration to Results.txt
    results_file.write(f"RESULTS FOR {date} SIMULATION")
    results_file.write("\n")
    results_file.write("\n** BEAM PROPERTIES **")
    results_file.write(f"\n    -- Beam Width:                          {beam_size} m")
    results_file.write(f"\n    -- Beam Starting Position:              [{round(beam_init_position[0],2)}, {round(beam_init_position[1],2)}] m")
    results_file.write(f"\n    -- Circular Raster Radius:              {circ_r} m")
    results_file.write(f"\n    -- XY Raster Radius:                    {xy_r} m")
    results_file.write(f"\n    -- Circular Raster Angular Velocity:    {circ_omega} Hz")
    results_file.write(f"\n    -- XY Raster Angular Velocity:          {xy_omega} Hz")

    # MAIN SIMULAITON
    print(f"Starting Simulation: {total_runs} runs")
    main_timer_start = time.perf_counter()
    
    while run_num < total_runs+1:
        
        # Set up parameters and detection data
        beam.Time = 0
        hit_time = []
        hit_counter = 0
        
        results_file.write("\n")
        results_file.write("\n--------------------------------------------------------------")
        results_file.write(f"\nStarting Run {run_num}")
        
        # Set Object Configuration
        # NEED TO SET UP PUNCH CARDS AND READ IN?
        ob_diameter = 0.18                                          # in meters
        ob_reflectance = 1                                      # unknown units
        ob_altitude = 500000                                        # in meters
        ob_init_position, ob_velocity = oc.TrajectoryGenerator(frame, 
                                                               fov,
                                                              7650, 
                                                              22.5, 
                                                              ob_altitude)
        ob = oc.Object(ob_diameter, ob_init_position, ob_velocity, 
                       ob_reflectance, ob_altitude)
        # Write object configuration results to Results.txt
        results_file.write("\n")
        results_file.write("\n** OBJECT PROPERTIES **")
        results_file.write(f"\n    -- Object Diameter:     {ob_diameter*100} cm")
        results_file.write(f"\n    -- Initial Position:    [{round(ob_init_position[0],2)},{round(ob_init_position[1],2)}] m")
        results_file.write(f"\n    -- Object Altitude:     {ob_altitude} m")
        results_file.write(f"\n    -- Object Velocity:     [{round(ob_velocity[0],2)},{round(ob_velocity[1],2)}] m/s")
        results_file.write(f"\n    -- Object Reflectance: {ob_reflectance}")
    
        sim_flags = fc.BoundaryFlags(ob.position, fov, 2)
        run_timer_start = time.perf_counter()
        
        print(f"Starting Run {run_num}")
        location_file.write(f"\n# RUN {run_num}")
        while sim_flags[1] == False:
            
            ob.move(time_step)
            beam.move(time_step, fov)
            
            if CollisionDetection(beam, ob) == True:
                hit_time.append(beam.Time)
                hit_counter += 1
                
            location_file.write(f"\n{beam.Time}, {beam.position}, {ob.position}")
            
            sim_flags = fc.BoundaryFlags(ob.position, fov, 2, sim_flags)
        
        # Process Run results
        elapsed_run_time = round((time.perf_counter() - run_timer_start), 3)
        
        results_file.write("\n")
        results_file.write("\n** RUN RESULTS **")
        results_file.write(f"\n    -- Run Time:                 {elapsed_run_time}")
        results_file.write(f"\n    -- Number of Detections:     {hit_counter}")
        results_file.write("\n    -- Detection Times:")
        for t in hit_time:
            results_file.write(f"\n        {t}")
        
        run_num += 1
    
    print("Ending Simulation")
    location_file.close()
    
    elapsed_main_time = round((time.perf_counter() - main_timer_start), 2)    
    
    results_file.write("\n")
    results_file.write("\n------------------------------------------------------------------")
    results_file.write("\n** FINAL RESULTS **")
    results_file.write(f"\nSimulation Time:    {elapsed_main_time} s")
    # print(f"Memory Usage:       {memMb} MB")
    if args.verbose == True:
        print("You've discovered the secret!")
    
    results_file.close()
        
if __name__=="__main__":
    main()