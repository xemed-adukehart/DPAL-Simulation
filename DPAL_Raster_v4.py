#!/usr/bin/python
import pylab as pl
import numpy as np
import random as rand
import time
import resource
import sys
from matplotlib.patches import RegularPolygon
from math import pi, cos, sin, sqrt
from prettytable import PrettyTable

pl.matplotlib.use('Qt5Agg')

#######################################################################################################
############################################ DEFINE CLASSES ###########################################
#######################################################################################################

class Object:
    def __init__(self, diam, pos, vel, alt, refl):
        self.internal_time = 0
        self.diam = diam
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.alt = alt
        self.refl = refl
        self.init_pos = np.array(pos)
        self.patch = pl.Circle((self.pos), self.diam/2, fc='black', ec='black')

    def move(self, dt):
        self.internal_time += dt

        new_pos = self.init_pos + self.vel*self.internal_time 

        self.pos = new_pos
        self.patch = pl.Circle((self.pos), self.diam/2, fc='black', ec='black')
        return self

class Beam:
    def __init__(self, size, pos, r_circ, r_xy, Omega, omega_x, omega_y):
        self.internal_time = 0
        self.size = size 
        self.pos = np.array(pos)
        self.r_circ = r_circ
        self.r_xy = r_xy
        self.Omega = Omega
        self.omega_x = omega_x
        self.omega_y = omega_y
        self.init_x = pos[0] 
        self.init_y = pos[1] 
        self.patch = RegularPolygon(self.pos, 4, radius=self.size/sqrt(2), fc='none', ec='blue', lw=2)

    def move(self, dt):
        self.internal_time = self.internal_time + dt

        x_circ, y_circ = Circle_Raster(self.r_circ, self.Omega, 0, self.internal_time)
        x_xy, y_xy = XY_Raster(self.r_xy, self.omega_x, self.omega_y, self.internal_time)

        new_pos = (np.array([500, 500]) + Circle_Raster(self.r_circ, self.Omega, 0, self.internal_time) 
                   + XY_Raster(self.r_xy, self.omega_x, self.omega_y, self.internal_time))
        self.pos = new_pos
        self.patch = RegularPolygon(self.pos, 4, radius=self.size/sqrt(2), fc='blue', ec='blue', lw=2)
        return self

#######################################################################################################
#######################################################################################################
#######################################################################################################

def Circle_Raster(R, omega, phi, dt):
    x = R*cos(omega*dt + phi)
    y = R*sin(omega*dt + phi)
    return np.array([x,y])


def XY_Raster(R, omega1, omega2, dt):
    x = R*(0.8106*cos(omega1*dt) + 0.0901*cos(3*omega1*dt) + 0.0324*cos(5*omega1*dt) 
           + 0.0165*cos(7*omega1*dt) + 0.01*cos(9*omega1*dt) + 0.0067*cos(11*omega1*dt) 
           + 0.0048*cos(13*omega1*dt) + 0.0036*cos(15*omega1*dt) + 0.0028*cos(17*omega1*dt) 
           + 0.0022*cos(19*omega1*dt))
    y = R*(0.8106*cos(omega2*dt) + 0.0901*cos(3*omega2*dt) + 0.0324*cos(5*omega2*dt) 
           + 0.0165*cos(7*omega2*dt) + 0.01*cos(9*omega2*dt) + 0.0067*cos(11*omega2*dt) 
           + 0.0048*cos(13*omega2*dt) + 0.0036*cos(15*omega2*dt) + 0.0028*cos(17*omega2*dt) 
           + 0.0022*cos(19*omega2*dt))
    return np.array([x, y])

#######################################################################################################

def fov_calculator(frame, p):
    x_min = (1 - p) * frame[0][0] + p * frame[0][1]
    x_max = p * frame[0][0] + (1 - p) * frame[0][1]
    y_min = (1 - p) * frame[1][0] + p * frame[1][1]
    y_max = p * frame[1][0] + (1 - p) * frame[1][1]

    return [[x_min, x_max], [y_min, y_max]]

#######################################################################################################

def rand_vel_gen():
    theta = 2 * pi * rand.random()
    speed = rand.gauss(7650, 22.5)

    return np.array([speed * cos(theta), speed * sin(theta)])


def rand_pos_gen(frame, fov):
    while True:
        X = rand.uniform(frame[0][0], frame[0][1])
        Y = rand.uniform(frame[1][0], frame[1][1])
        if not (fov[0][0] < X < fov[0][1]):
            return np.array([X, Y])
        elif not (fov[1][0] < Y < fov[1][1]):
            return np.array([X, Y])


def check_trajectory(pos, vel, frame, fov):
    length = frame[0][1] - frame[0][0]
    height = frame[1][1] - frame[1][0]
    t_max2 = (length**2 + height**2) / (vel[0]**2 + vel[1]**2)
    t_max = sqrt(t_max2)

    for t in np.arange(0, t_max, 0.1):
        if ((fov[0][0] < pos[0] + vel[0]*t < fov[0][1]) 
            and (fov[1][0] < pos[1] + vel[1]*t < fov[1][1])):
                return True

    return False


def gen_trajectory(frame, fov):
    test_pos = rand_pos_gen(frame, fov)

    while True:
        test_vel = rand_vel_gen()
        if check_trajectory(test_pos, test_vel, frame, fov) == True:
            return test_pos, test_vel

#######################################################################################################

def boundary_flags(pos, fov, flags=None):
    if flags == None:
        enter_flag = False
        exit_flag = False
    else:
        enter_flag = flags[0]
        exit_flag = flags[1]

    x, y = pos[0], pos[1]
    x_min = fov[0][0] - 2
    x_max = fov[0][1] + 2
    y_min = fov[1][0] - 2
    y_max = fov[1][1] + 2
    x_condition = x_min < x < x_max 
    y_condition = y_min < y < y_max 

    if x_condition == True and y_condition == True and enter_flag == False:
        enter_flag = True
    elif (x_condition == False or y_condition == False) and enter_flag == True:
        exit_flag = True

    return [enter_flag, exit_flag]

#######################################################################################################

def detect_collision(beam ,object1):
    ob1_r = object1.diam/2
    ob1_x = object1.pos[0]
    ob1_y = object1.pos[1]

    beam_x = beam.pos[0]
    beam_y = beam.pos[1]
    beam_size = beam.size

    dist2 = (ob1_x - beam_x)**2 + (ob1_y - beam_y)**2

    if dist2 <= (ob1_r+beam_size)**2:
        return True
    else:
        return False

    
#######################################################################################################
#######################################################################################################
#######################################################################################################

def main():
    time_start = time.perf_counter()

    simulation_hist = {}

    run_num = 1
    total_runs = 10

    print("Initializing...")
    frame = [[-1000, 2000], [-1000, 2000]]

    fov = fov_calculator(frame, 1/3)
    fig = pl.figure()
    ax = pl.axes(xlim=fov[0], ylim=fov[1], aspect='1')
    ax.tick_params(axis='both', which='both',
                   bottom=False,
                   left=False,
                   labelbottom=False,
                   labelleft=False)
    ax.set_title('Field of View')

    beam_width = 2
    beam_init_pos = [((fov[0][0] + fov[0][1])/2), ((fov[1][0] + fov[1][1])/2)]
    xy_rast_r = 195.12 
    circ_rast_r = 304.88 
    x_rast_v = 2305 
    y_rast_v = 990 
    circ_rast_v = 23230

    ### Beam(beam_diam, beam_init_pos, circ_rast_r, xy_rast_r, circ_rast_v, x_rast_v, y_rast_v):
    beam = Beam(beam_width, beam_init_pos, circ_rast_r, xy_rast_r, circ_rast_v, x_rast_v, y_rast_v)
    print("")
    print("** Beam Properties **")
    print(f"    -- Beam Width:                          {beam_width} m")
    print(f"    -- Beam Starting Position:              [{round(beam_init_pos[0],2)}, {round(beam_init_pos[1],2)}] m")
    print(f"    -- Circular Raster Radius:              {circ_rast_r} m")
    print(f"    -- XY Raster Radius:                    {xy_rast_r} m")
    print(f"    -- Circular Raster Angular Velocity:    {circ_rast_v}")
    print(f"    -- XY Raster Angular Velocity:          [{x_rast_v},{y_rast_v}]")
    print("")
  

    while run_num < total_runs+1: 
        time_start_run = time.perf_counter()
        beam.internal_time = 0
        b_detect_loc = []
        o_detect_loc = []
        time_detect = []
        
        print("--------------------------------------------------------------------------------------")
        print(f"STARTING RUN {run_num}")
        time_step = 0.0000009 
        hit_counts = 0

        print("")
        ob_diam = 0.18
        ob_refl = 1
        ob_alt = 500000
        init_pos, vel = gen_trajectory(frame, fov)
        ob = Object(ob_diam, init_pos, vel, ob_alt, ob_refl)
        print("** Object Properties **")
        print(f"    -- Object Diameter:     {ob_diam*100} cm")
        print(f"    -- Initial Position:    [{round(init_pos[0],2)},{round(init_pos[1],2)}] m")
        print(f"    -- Object Velocity:     [{round(vel[0],2)},{round(vel[1],2)}] m/s")
        print(f"    -- Object Altitude:     {ob_alt} m")
        print(f"    -- Object Reflectivity: {ob_refl}")
    
        ax.add_patch(ob.patch)
        ax.add_patch(beam.patch)
        sim_flags = boundary_flags(ob.pos, fov)

        while sim_flags[1] == False:
            ob.move(time_step)
            beam.move(time_step)
            if detect_collision(beam, ob) == True:
                b_detect_loc.append([round(beam.pos[0],3),round(beam.pos[1],3)])
                o_detect_loc.append([round(ob.pos[0],3),round(ob.pos[1],3)])
                time_detect.append(round(beam.internal_time,2))
                hit_counts += 1
            sim_flags = boundary_flags(ob.pos, fov, sim_flags)

        time_elapsed_run = round((time.perf_counter() - time_start_run), 2)

        print("")
        print("** Run Results **")
        print(f"    -- Number of Detections:     {hit_counts}")
        print(f"    -- Run Time:                 {time_elapsed_run}")
        ## ADD TABLE OF LOCATIONS WHEN A DETECTION OCCURED!! ##
        table = PrettyTable()
        table.field_names = ['Beam Local', 'Object Local', 'Time']
        for i in range(len(time_detect)):
            table.add_row([b_detect_loc[i], o_detect_loc[i], time_detect[i]])
        print("")
        print("    -- List of Detections:")
        print(table)


        print("")

        simulation_hist.update({f"Run {run_num}": hit_counts}) 
        run_num += 1

    print("--------------------------------------------------------------------------------------")

    time_elapsed = round((time.perf_counter() - time_start), 2)
    memMb = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0/1024.0, 3)

    print("** Final Results **")
    print(f"Simulation Time:    {time_elapsed} s")
    print(f"Memory Usage:       {memMb} MB")
    print(simulation_hist)
#    pl.show()
    
if __name__=="__main__":
    main()
