import smtplib
import subprocess
import datetime
import os
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException
from twilio import TwilioException
#import !/usr/local/lib/python2.7/dist-packages/twilio-5.4.0-py2.7.egg/twilio


#send is the main function to be called from the driver process, and
#sends the text passed in 'errorText' in an sms and email message to
#all users in the specified scope. Scope can be either 'freezer',
#'vivarium', or 'all', and is used to ensure, that users will recieve
#only the messages regarding the system they wish to know about. For
#example: freezer temperatue alerts should be called with the
#'freezer' scope variable. See test.py for proper use.

rootdir = os.path.abspath("..")

#Returns authenticated twilio rest object
def authenticate(errorFile):

	try:
		keyFile = open(rootdir+"/alertSrc/keys.txt",'r')
	except IOError:
		date = datetime.datetime.now()
		errorFile.write(date.isoformat(" ") + ": Could not find key file\n")
		return -1

	date = datetime.datetime.now()
	errorFile.write(date.isoformat(" ") + ": Alert module called\n")

	#read keys from key file and strip newlines (hence [:-1])
	test_sid   = keyFile.readline()[:-1]
	test_token = keyFile.readline()[:-1]

	prod_sid   = keyFile.readline()[:-1]
	prod_token = keyFile.readline()[:-1]

	#select keys to use (test or production)
	sid   = prod_sid
	token = prod_token

	try:
		client = TwilioRestClient(sid, token)
		return sid, token, client

	except TwilioException as e:
		date = datetime.datetime.now()
		errorFile.write(date.isoformat(" ") + ": Could not register Twilio client\n")
		return -1

def send(errorText, scope):

	returnval = 0

	errorFile = open(rootdir+"/logs/alertlogs.txt",'a')

	sid, token, client = authenticate(errorFile)

	#send alerts
	returnval += sms_alert  (sid, token, client, errorText)

	if returnval == -2:
		date = datetime.datetime.now()
		errorFile.write(date.isoformat(" ") + ": Error in sms_alert\n")

	returnval += email_alert(sid, token, client, errorText)
	if returnval == -1 or returnval == -3:
		date = datetime.datetime.now()
		errorFile.write(date.isoformat(" ") + ": Error in email_alert\n")

	return returnval

#alert mobile users. Return -2 on failure.
def sms_alert(sid, token, client, errorText):

	returnval = 0
	#read users
	userFile = open(rootdir + "/alertSrc/user_register/phone.txt", 'r')
	users = []

	#load file into list
	for line in userFile:
		users.append(line)

	for user in users:
		userList = str.split(user)

		#For each user with the appropriate scope
		if(userList[1] == "all" or userList[1] == scope):

			try:
				client.messages.create(
					to   = userList[0],
					from_="+13609001272",
					body = "\"" + errorText + "\""
				)
			except TwilioRestException as e:
				#note: will return -1 even if only one message fails
				returnval = -2

	return returnval

#alert email users. Retiurn -1 on failure.
def email_alert(sid, token, client, errorText):
	#read users
	userFile = open(rootdir + "/home/pi/frosti/alertSrc/user_register/email.txt", 'r')
	users = []
	recipString = ''

	#load file into list
	for line in userFile:
		users.append(line)

	for user in users:
		userList = str.split(user)

		#Add each user in scope to the recipient list
		if(userList[1] == "all" or userList[1] == scope):
			recipString = recipString + userList[0] + " "

	try:
		subprocess.call('echo  ' + "\"" + errorText + "\"" + '| mail -s ' + "\"NEW ALERT FROM FROSTI: \"" + ' ' +  recipString,shell=True)
	except OSError as e:
		return -1

	return 0
