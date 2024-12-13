#!/usr/bin/env python
"""
Created on Tue Nov 26 13:35:17 2024

@author: adukehart
"""

import pylab as pl
import numpy as np
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers
from tkinter import filedialog
from ast import literal_eval

#pl.matplotlib.use('Qt5Agg')

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
data = pd.read_csv(file_path)

b_local = [literal_eval(x) for x in data['Beam Location']]

fig = plt.figure()
ax = plt.axes(xlim=(-500,500), ylim=(-500,500))
ax.set_title('Field of View')

def animate(i):
    beam = ax.add_patch(plt.Circle((b_local[i][0], b_local[i][1]), 2))
    return beam

ani = FuncAnimation(fig, animate, frames=len(b_local), interval=1, blit=False)

print("Directing Movie")
Writer = writers['ffmpeg']
writer = Writer(fps=60, bitrate=1000)
ani.save(file_path, writer=writer)
print("Releasing Movie")