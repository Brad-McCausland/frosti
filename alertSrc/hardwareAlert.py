#This is a simple script to bridge the gap between
#the C netcode and the rest of the python source.
#Specifically the alert module.

import sys
import datetime

from alert import *

message = sys.argv[1]

date = datetime.datetime.now()
errorFile = open("/home/pi/frosti/logs/hardwarealertlogs.txt",'a')
errorFile.write(date.isoformat(" ") + ": Hardware alert with message: '" + message + "'\n")

send(message, "all")

