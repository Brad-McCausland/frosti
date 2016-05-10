#!/usr/bin/env python

# Scott St. John
# 4/24/16 
# CSCI 492: Senior Project
# thermistor.py
#

# Simple data container object

class Thermistor (object):

        def __init__(self, iD, pinNum):
            self.iD = iD
            self.pinNum = pinNum
            self.readings = [0]*10
            self.averageReading = 0
            self.currentTemp = 0

