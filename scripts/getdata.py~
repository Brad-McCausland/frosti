import csv
import datetime
import os
import sys
import string
import subprocess

def main():
	try:
		date  = sys.argv[1]
		email = sys.argv[2]
	except IndexError as e:
		date  = raw_input("Please enter the date (YYYY/MM/DD) of the data you would like to examine: ")
		email = raw_input("Please enter the email address you would like me to forward the data to: ")

	date   = date.replace("/", "-")

	message  = "FROSTI data on the day of " + date
	filename = date+".csv"
	#path     = "/home/pi/frosti/logs/"+filename
	path     = "/home/bmcc0605/frosti/frosti/logs/"+filename #test path

	try:
		subprocess.call('uuencode '+path+' '+filename+' | mail -s NEW MESSAGE FROM FROSTI ' +  email,shell=True)
		print("Success: data for the day "+date+" has been forwarded to "+email)
	except OSError as e:
		print("Error: Could not send email")

main()
