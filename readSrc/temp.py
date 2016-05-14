#!/usr/bin/env python

# Scott St. John
# 4/24/16 
# CSCI 492: Senior Project
# temp.py
#

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

# Module calulates the temperature

from __future__ import division
from thermistor import Thermistor
import read

#Resistance in Ohms at 25 C (50K)
nominalResistance = 50000

#the value of the 'other' resistor
seriesResistance = 10000  

#25 degress C
nominalTemperature = 25

#don't know if this is correct
betaCoefficient = 3917.93

#number of thermistors
numThermistors = 6

#number of sample for a reading
numSamples = 10

#list of all thermistors
thermistorList = []

def thermistors_init():
    for i in range(0, numThermistors):
        newThermistor = Thermistor(i, i)
        thermistorList.append(newThermistor)

# calcTemp()
#   Function reads values from the appropriate thermistor pin.
#   Takes an average of the reading.
#   Calculates the temperature using B parameter equation:
#             1/T = 1/T_0 + 1/B*ln(R/R_0)
#
def calc_temp():
    for thermistor in thermistorList:
        resistance = 0
        steinhart = 0
        
        for i in range(0, numSamples):
            thermistor.readings[i] = read.readAdc(thermistor.pinNum, read.SPICLK,
                                                  read.SPIMOSI, read.SPIMISO, read.SPICS)
            read.time.sleep(1)
            
        for i in range(0, numSamples):
            thermistor.averageReading += thermistor.readings[i]
            
        thermistor.averageReading /= numSamples
        print("Average analog reading for Thermistor: %d is %d\n"
              % (thermistor.iD, float(thermistor.averageReading))) 

        resistance = 1023/thermistor.averageReading - 1
        resistance = seriesResistance/resistance
        print("Thermistor resistance: %d\n" % resistance)

        steinhart = resistance/nominalResistance
        steinhart = read.math.log(steinhart)
        steinhart /= betaCoefficient
        steinhart += 1.0/(nominalTemperature + 273.15) # + (1/To)
        steinhart = 1.0/steinhart                #Invert
        steinhart -= 273.15

        print("Temperature: %d degrees C\n" % steinhart)
        print("Temperature: %d degrees F\n" % (steinhart*9/5 + 32))
        
    
