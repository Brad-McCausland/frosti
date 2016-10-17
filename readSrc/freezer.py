#!/usr/bin/python3

# Scott St. John
# 5/14/16 
# CSCI 492: Senior Project
# freezer.py
#

# Simple data container object

from thermistor import Thermistor

class Freezer (object):

        def __init__(self, iD):
            self.iD = iD
            self.thermistorList = []

