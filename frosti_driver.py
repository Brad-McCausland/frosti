# FROSTi Driver

from temp import *
from log import *
from alert import *
import datetime

#IP address of other pi
#init other

#true if active pi
active = true
    
def run():
    if active:
        for freezer in range (0,3):
            time = datetime.datetime.now()
            temp = read(freezer)
            n = log(freezer, temp)
            if n == -1:
                #error
            if data.temp > -60.0:
                error = "Warning: Freezer " + freezer + " has reached " + temp + " at " + time + "."
                n = send(error, "freezer")
                if n == -1:
                    #email error
                elif n == -2:
                    #text error
                elif n == -3:
                    #email and text error
        check_partner(other)

def check_partner(other):
    #ping other
    if fail:
        #ping again, break if success
        active = true
        error = "Warning: Pi " + other + " is down. Please replace soon."
        n = send(error, "all")
        if n == -1:
            #email error
        elif n == -2:
            #text error
        elif n == -3:
            #email and text error
    
