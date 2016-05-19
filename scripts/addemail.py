#!/usr/bin/env python

import sys
import string
import os

def main():
	address = sys.argv[1]
	scope  = sys.argv[2]

	if '@' not in address:
		print("Error: please enter a valid email address (missing '@')")
		return

	scope = scope.lower()

	if scope != "all" and scope != "freezer" and scope != "vivarium":
		print "Error: scope '"+scope+"' not recognized (accepted values are 'all', 'freezer', and 'vivarium')"
		return

	emailFile = open(os.path.join(os.path.expanduser('~'),"frosti/frosti/alertSrc/user_register/email.txt"), 'a+')

	for line in emailFile:
		if address in line:
			print "Error: This email address is already registered in our email directory!"
			return

	emailFile.write(address+" "+scope)

	print address+" will now be sent "+scope+" messages!"

main()
