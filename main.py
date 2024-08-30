#!/usr/bin/env python
"""
Created on Fri Jul 19, 2024

@author: adukehart
"""

import time
import Modules.FrameClass as fc
import Modules.BeamClass as bc
import Modules.ObjectClass as oc
import random as rand
from prettytable import PrettyTable
import matplotlib.pyplot as plt
from Modules.Collision import CollisionDetection

rand.seed(10)

def main():
    timer_start = time.perf_counter()
    
    # Set Simulation Parameters
    results = {}
    run_num = 1
    total_runs = 1
    time_step = 0.0000001                                           # in sec
    
    # Set Frame configuration
    frame = fc.Frame(3000, 3000)                                    # in meters
    fov = frame.make_fov(1/3)
    
    # Set Beam Configuration
    beam_size = 2                                                   # in meters
    beam_init_position = fov.get_center()
    circ_r = 304.88                                                 # in meters
    xy_r = 195.12                                                   # in meters
    circ_omega = 23230                                              # in Hz
    xy_omega = [2305, 990]                                          # in Hz
    beam = bc.Beam(beam_size, beam_init_position, 
                   circ_r, xy_r, 
                   circ_omega, xy_omega)

    print("")
    print("** BEAM PROPERTIES **")
    print(f"    -- Beam Width:                          {beam_size} m")
    print(f"    -- Beam Starting Position:              [{round(beam_init_position[0],2)}, {round(beam_init_position[1],2)}] m")
    print(f"    -- Circular Raster Radius:              {circ_r} m")
    print(f"    -- XY Raster Radius:                    {xy_r} m")
    print(f"    -- Circular Raster Angular Velocity:    {circ_omega} Hz")
    print(f"    -- XY Raster Angular Velocity:          {xy_omega} Hz")
    print("")
    
    # Main Simulation
    while run_num < total_runs+1:
        run_Timer = time.perf_counter()
        
        beam.Time = 0
        
        # Record Detection Data
        beam_loc = []
        ob_loc = []
        hit_time= []
        
        print("--------------------------------------------------------------")
        print(f"Starting Run {run_num}")
        print("")
        
        hit_counts = 0
        
        # Set Object configuration
        ob_diameter = 0.18                                          # in meters
        ob_reflectance = 1                                      # unknown units
        ob_altitude = 500000                                        # in meters
        ob_init_position, ob_velocity = oc.TrajectoryGenerator(frame, fov,
                                                              7650, 22.5, 
                                                              ob_altitude)
        ob = oc.Object(ob_diameter, ob_init_position, ob_velocity, 
                       ob_reflectance, ob_altitude)
        print("** OBJECT PROPERTIES **")
        print(f"    -- Object Diameter:     {ob_diameter*100} cm")
        print(f"    -- Initial Position:    [{round(ob_init_position[0],2)},{round(ob_init_position[1],2)}] m")
        print(f"    -- Object Velocity:     [{round(ob_velocity[0],2)},{round(ob_velocity[1],2)}] m/s")
        print(f"    -- Object Reflectance: {ob_reflectance}")
        print(f"    -- Object Altitude:     {ob_altitude} m")
        print("")
        
        n = 0
        t = 0
        sim_flags = fc.BoundaryFlags(ob.position, fov, 2)
        
        while sim_flags[1] == False:
            ob.move(time_step)
            beam.move(time_step, fov)
            if t%1000 == 0:
                xmin, xmax, ymin, ymax = fov.get_axis()
                fig, ax = plt.subplots()
                fig.suptitle(f'Field of View: t = {t}s')
                ax.set_xlim((xmin, xmax))
                ax.set_ylim((ymin, ymax))
                ax.tick_params(axis='both', which='both',
                                   bottom=False,
                                   left=False,
                                   labelbottom=False,
                                   labelleft=False)
                ax.set_aspect('equal')
                ob.render(ax)
                beam.render(ax)
                fig.savefig(f'frame_{n}')
            
            if CollisionDetection(beam, ob) == True:
                beam_loc.append([round(beam.position[0],3), 
                                 round(beam.position[1],3)])
                ob_loc.append([round(ob.position[0],3), 
                               round(ob.position[1], 3)])
                hit_time.append(round(beam.Time, 2))
                hit_counts += 1
            n += 1
            t += 1
            sim_flags = fc.BoundaryFlags(ob.position, fov, 2, sim_flags)
            
        elapsed_time_run = round((time.perf_counter() - run_Timer), 2)
        
        table = PrettyTable()
        table.field_names = ['Beam Local', 'Object Local', 'Time']
        for i in range(len(hit_time)):
            table.add_row([beam_loc[i], ob_loc[i], hit_time[i]])
        
        print("** RUN RESULTS **")
        print(f"    -- Number of Detections:     {hit_counts}")
        print(f"    -- Run Time:                 {elapsed_time_run}")
        print("")
        print("    -- List of Detections:")
        print(table)
        print("")
        
        results.update({f"Run {run_num}": hit_counts})
        run_num += 1
        
    print("------------------------------------------------------------------")
        
    elapsed_time = round((time.perf_counter() - timer_start), 2)
    # ADD MEMORY USAGE DATA
        
    print("** FINAL RESULTS **")
    print(f"Simulation Time:    {elapsed_time} s")
    # print(f"Memory Usage:       {memMb} MB")
    print(results)
        
    
if __name__=="__main__":
    main()