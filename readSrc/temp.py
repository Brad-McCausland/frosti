#!/usr/bin/python3

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
from freezer import Freezer
import read

#Resistance in Ohms at 25 C (50K)
nominalResistance = 50000

#the value of the 'other' resistor
seriesResistance = 10000000  

#25 degress C
nominalTemperature = 25

#number of freezers
#number 0,1 are same/small freezer
#number 2 is the star wars freezer
numFreezers = 3

#number of thermistors per freezer
#thermistors 0-3 belong to small freezer
#thermistors 4-5 belong to star wars freezer
numThermistors = 2

#number of sample for a reading
numSamples = 50

#list of all freezers
freezerList = []

#array of beta coefficients
betas = [2498.05, 2501.01, 2556.60, 2537.25, 2621.25, 2649.95]

def freezers_init():
    for i in range(0, numFreezers):
        newFreezer = Freezer(i)
        freezerList.append(newFreezer)

def thermistors_init():
    idNum = 0
    for freezer in freezerList:
        for i in range(0, numThermistors):
            newThermistor = Thermistor(idNum, idNum)
            freezer.thermistorList.append(newThermistor)
            idNum = idNum + 1

# calcTemp(Freezer freezer)
#   Function reads pin readings for the freezer given
#   Takes an average of the readings.
#   Calculates the temperature using B parameter equation:
#             1/T = 1/T_0 + 1/B*ln(R/R_0)
#   Returns the average of the two temperatures for the freezer
#
def calc_temp(freezerNum):

    for thermistor in freezerList[freezerNum].thermistorList:
        resistance = 0
        steinhart = 0
        
        #print(type(thermistor) is Thermistor)
        for i in range(0, numSamples):
            thermistor.readings[i] = read.readAdc(thermistor.pinNum, read.SPICLK,
                                                  read.SPIMOSI, read.SPIMISO, read.SPICS)
            read.time.sleep(0.1)
            
        for i in range(0, numSamples):
            thermistor.averageReading += thermistor.readings[i]
            
        thermistor.averageReading /= numSamples

        resistance = 1023/(thermistor.averageReading - 1)
        resistance = seriesResistance / resistance
        
        betaCoefficient = betas[thermistor.pinNum]
                
        steinhart = resistance/nominalResistance
        steinhart = read.math.log(steinhart)
        steinhart /= betaCoefficient
        steinhart += 1.0/(nominalTemperature + 273.15) # + (1/To)
        steinhart = 1.0/steinhart                #Invert
        steinhart -= 273.15

        thermistor.currentTemp = steinhart
    
    temp1 = freezerList[freezerNum].thermistorList[0].currentTemp
    temp2 = freezerList[freezerNum].thermistorList[1].currentTemp
    averageTemp = (temp1 + temp2)/2
    return averageTemp

def calc_temp_simple(resistance, beta):
    steinhart = resistance/nominalResistance
    steinhart = read.math.log(steinhart)
    steinhart /= beta
    steinhart += 1.0/(nominalTemperature + 273.15) # + (1/To)
    steinhart = 1.0/steinhart                #Invert
    steinhart -= 273.15
    return steinhart

def calc_beta(resistance):
    acceptedBetas = []
    step = 0.10
    i = 0
    beta = 1000.00
    while beta < 4500:
        temp = calc_temp_simple(resistance, beta)
        if temp < -79.99 and temp > -80.01:
            acceptedBetas.append(beta)
        beta = beta + step
    finalBeta = sum(acceptedBetas)/len(acceptedBetas)
    return finalBeta

def calc_beta_alt(resistance):
    acceptedBetas = []
    step = 0.10
    i = 0
    beta = 1000.00
    while beta < 4500:
        temp = calc_temp_simple(resistance, beta)
        if temp < -82.99 and temp > -83.01:
            acceptedBetas.append(beta)
        beta = beta + step
    finalBeta = sum(acceptedBetas)/len(acceptedBetas)
    return finalBeta
