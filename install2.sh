#!/bin/bash

#part two of installer. to be run without sudo

#set cron jobs

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -a|--active)
    ACTIVE="$2"
    shift # past argument
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done

cd ~
crontab -l > mycron
if [ $ACTIVE == "yes" -o $ACTIVE == "y" ]
then
	echo "*/5 * * * * python /home/pi/frosti/frosti_driver.py" >> mycron
else
	echo "*/5 * * * * python /home/pi/frosti/testDriver.py" >> mycron
fi
echo "1-59/15 * * * * /home/pi/frosti/netSrc/frosti_client 127.0.0.1 8001" >> mycron

#The idea here is to send a message at noon on the 1st and 15th of each month. Might be bad syntax
echo "0 12 1,15 * * python /home/pi/frosti/alertSrc/twilioKeepAlive.py" >> mycron
crontab mycron
rm mycron

echo "cron job added. Don't forget to enter my counterpart's ip in crontab! Did you install twilio? Mailutils?"
