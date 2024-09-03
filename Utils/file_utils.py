#!/usr/bin/env python
"""
Created on Fri Aug 30 09:12:44 2024

@author: adukehart
"""

def readFile(PATH_TO_FILE):
    with open(PATH_TO_FILE, 'r') as file:
        return file.read()
    
def writeFile(PATH_TO_FILE, content):
    with open(PATH_TO_FILE, 'w') as file:
        file.write(content)