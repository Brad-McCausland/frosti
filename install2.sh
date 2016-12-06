#!/bin/bash

#part two of installer. to be run without sudo

#set cron jobs

echo "Will this be the active pi (will it be running the webserver?) y/n"

read ACTIVE

cd ~
crontab -l > mycron
if [ $ACTIVE == "y" ]; then
	echo "*/5 * * * * python /home/pi/frosti/frosti_driver.py" >> mycron
	echo "0 12 1,15 * * python /home/pi/frosti/alertSrc/twilioKeepAlive.py" >> mycron
elif [ $ACTIVE == "n" ]; then
	# run inactive driver (subject to change)
	echo "*/5 * * * * python /home/pi/frosti/testDriver.py" >> mycron

	# sync contact info with active pi
	echo "0 0 * * * /home/pi/frosti/alertSrc/sync_contacts" >> mycron

	# remove duplicate web server
	sudo rm /etc/init.d/startFrostiWeb.sh
else
	echo "Please enter either y or n. Aborting installer."
	exit 1
fi

echo "1-59/15 7-19 * * * /home/pi/frosti/netSrc/frosti_client 127.0.0.1 8001" >> mycron

crontab mycron
rm mycron

echo "cron job added. Don't forget to enter my counterpart's ip in crontab! Did you install twilio? Mailutils?"
