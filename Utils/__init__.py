#!/usr/bin/env python
"""
Created on Fri Aug 30 12:40:01 2024

@author: adukehart
"""

# This code will be executed when the simulation package is imported
print("Loading Utilities")

# Import specific functions and classes from the simulation utilities
from .file_utils import readFile, writeFile
from .datetime_utils import formatDate, getCurrentDate

# Define the available classes and functions when using
__all__ = ['readFile',
           'writeFile', 
           'formatDate',
           'getCurrentDate']

# Define version number
__version__ = '0.0.1'