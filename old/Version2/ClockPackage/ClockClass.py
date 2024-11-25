#!/usr/bin/env python
"""
Created on Wed Sep  4 10:20:03 2024

@author: adukehart
"""

class Clock:
    def __init__(self):
        self.Time = 0
        
    def tick(self, dt):
        self.Time = self.Time + dt
        
    def reset(self):
        self.Time = 0