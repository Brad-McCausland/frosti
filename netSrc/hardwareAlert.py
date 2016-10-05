#This is a simple script to bridge the gap between
#the C netcode and the rest of the python source.
#Specifically the alert module.

import sys
import os

sys.path.insert(0, "../alertSrc/")

from alert import *

os.chdir("../alertSrc/")

message = sys.argv[1]

send(message, "all")
