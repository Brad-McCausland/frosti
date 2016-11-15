# Calls hardware alert and sends a message given as arg 1
# Meant to be hooked up to the web portal so that users
# can verify that messaging is still working, or send
# announcements if needed.

import sys
from subprocess import call

message = ""
try:
	message = sys.argv[1]
except:
	print "Error: one argument needed (message contents)"

call(["python", "../alertSrc/hardwareAlert.py", message]);
