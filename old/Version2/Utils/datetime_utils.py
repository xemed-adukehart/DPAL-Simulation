# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 17:01:19 2024

@author: adukehart
"""

from datetime import datetime

def formatDate(date, format='%d-%m-%Y_%H.%M.%S'):
    return date.strftime(format)

def getCurrentDate():
    return datetime.now()