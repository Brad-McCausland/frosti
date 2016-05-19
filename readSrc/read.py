#!/usr/bin/env python

# Scott St. John
# 4/24/16 
# CSCI 492: Senior Project
# read.py
#

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

# Module initializes the GPIO PINS on the Pi and reads the ADC

import time
import os
import math
import  python3-rpi.gpio as GPIO

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 23 #18
SPIMISO = 21 #23
SPIMOSI = 19 #24 
SPICS = 24 #25

DEBUG = 1

def gpio_init():
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # set up the SPI interface pins
        GPIO.setup(SPIMOSI, GPIO.OUT)
        GPIO.setup(SPIMISO, GPIO.IN)
        GPIO.setup(SPICLK, GPIO.OUT)
        GPIO.setup(SPICS, GPIO.OUT)

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readAdc(adcNum, clockPin, mosiPin, misoPin, csPin):
        if ((adcNum > 7) or (adcNum < 0)):
                return -1
        GPIO.output(csPin, True)

        GPIO.output(clockPin, False)  # start clock low
        GPIO.output(csPin, False)     # bring CS low

        commandOut = adcNum
        commandOut |= 0x18  # start bit + single-ended bit
        commandOut <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandOut & 0x80):
                        GPIO.output(mosiPin, True)
                else:
                        GPIO.output(mosiPin, False)
                commandOut <<= 1
                GPIO.output(clockPin, True)
                GPIO.output(clockPin, False)

        adcOut = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockPin, True)
                GPIO.output(clockPin, False)
                adcOut <<= 1
                if (GPIO.input(misoPin)):
                        adcOut |= 0x1

        GPIO.output(csPin, True)
        
        adcOut >>= 1       # first bit is 'null' so drop it
        return adcOut


    

    
