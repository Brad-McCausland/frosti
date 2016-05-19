#!/usr/bin/env python

import sys
import string
import os

def main():
	address = sys.argv[1]

	if '@' not in address:
		print("Error: please enter a valid email address (missing '@')")
		return


	#read file
	emailFile = open(os.path.join(os.path.expanduser('~'),"frostiSrc/alertSrc/user_register/email.txt"), 'r')
	lines = emailFile.readlines()
	emailFile.close()

	#open file for overwriting
	emailFile = open(os.path.join(os.path.expanduser('~'),"frostiSrc/alertSrc/user_register/email.txt"), 'w')

	#boolean set to true if matching number is found. Triggers 'number not found' message
	found = False
	
	for line in lines:
		if address not in line:
			#rewrite file
			emailFile.write(line)
		else:
			found = True
			#skip number to be deleted
			print("Email address "+address+" has been deleted from our email records!")

	if not found:
		print("Email address "+address+" was not found in our records (no changes made to file)")

main()
