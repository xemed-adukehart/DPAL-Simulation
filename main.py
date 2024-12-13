#!/usr/bin/env python
"""
Created on Fri Nov 22 14:41:27 2024

@author: adukehart

SEARCH AND DETECT:
    This program is designed to mimic the search and detect system intended for
    DPAL. A successful search and detect involves two detections of the same
    object. To simulate this, the program mimics a detection as a collision. If
    to collisions occur, each with an object with the same altitude, the search
    and detect mission is considered successful. Note, this operates on the
    assumption that each object has a unique altitude and the altitude is
    static.
"""

import gc
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from memory_profiler import profile
from BeamClass import Beam
from ObjectsClass import Objects
from ClockPackage import Clock
from Utils.Collision import Detect
from Utils.datetime_utils import formatDate, getCurrentDate

@profile
def Simulation():
    #SIMULATION PARAMETERS
    time_step = 0.000001
    total_runs = 5
    run = 0

    # Define generating frame and field of view (fov)
    frame = np.array([[-1500.0, 1500.0], [-1500.0, 1500.0]])
    fov = np.array([[-500.0, 500.0], [-500.0, 500.0]])
    boundary = np.array([[-750.0, 750.0], [-750.0, 750.0]])

    # Initialize DPAL Beam
    beam = Beam(Size = 2,
                R1 = 400.0,
                R2 = 100.0,
                ω1 = 25990,
                ω2 = 45130)

    # Initialize Simulation Clock
    sim_clock = Clock()

    avg_detections = []
    times = []
    # START SIMULATION
    while run < total_runs:
        start = time.time()
        sim_clock.reset()
        beam.reset()

        # Initialize LEO Objects
        obs = Objects(frame, fov, Num_Obs=10)

        # Initialize DataFrame
        headers = ['Simulation Time', 'Beam Location']
        headers.extend(f"Object{i} Location" for i in range(obs.number))
        data = []

        first_altitude = None
        shift = None
        detections = []
        print("Starting Run ", run+1)
        while any(x == 0 for x in obs.exit_flags):
            # If there hasn't been an initial detection
            if first_altitude == None:
                # Update Positions and Time
                beam.move(time_step, fov)
                obs.move(time_step)
                sim_clock.tick(time_step)
    
                # Update Object Flags
                obs.update_flags(boundary, 0)
                
                # Check for Collisions
                detection = Detect(beam, obs)
                if any(detection==True):
                    idx = np.where(detection==True)
                    first_altitude = obs.get_altitude(idx[0][0])
                    shift = obs.get_position(idx[0][0])
                    fov[:] += shift[:2]
                  
            else:
                # Need a 10ms pause for beam to "move"
                beam.move(time_step, fov)
                obs.move(time_step)
                sim_clock.tick(time_step)
            
                # Update Object Flags
                obs.update_flags(boundary, 0)
            
                # Check for Secondary Collisions
                detection = Detect(beam, obs)
                if any(detection==True):
                    idx = np.where(detection==True)
                    second_altitude = obs.get_altitude(idx[0][0])
                    if first_altitude == second_altitude:
                        detections.append(idx[0][0])
                        fov[:] -= shift[:2]
                        first_altitude = None
                    
            # Record Position Data and Time
            row = [sim_clock.Time, beam.get_position()]
            row.extend(obs.get_position(i) for i in range(obs.number))
            data.append(row)
        
        # Write data to CSV file
        position_data = pd.DataFrame(data=data, columns=headers)

        date = formatDate(getCurrentDate())
        position_data.to_csv(date+f"Run{run+1}.csv")
        
        
        end = time.time()
        times.append(end-start)
    
        avg_detections.append(len(detections))
#        gc.collect()
        run += 1

    print("Total Simulation Time: ", sum(times))
    print("Average Number of Successful Detections: ", sum(avg_detections)/len(avg_detections))
    print("Successful Detections ", avg_detections)
    plt.bar(range(len(times)), times)
    plt.title("Computation Times for Run X")
    
    plt.show()

if __name__ == '__main__':
    Simulation()    