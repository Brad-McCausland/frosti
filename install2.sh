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
echo "*/15 * * * * /home/pi/frosti/netSrc/frosti_client 127.0.0.1 8001" >> mycron
crontab mycron
rm mycron
