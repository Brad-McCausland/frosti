#!/bin bash

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

if [ $ACTIVE == "" ]
then
        echo "No argument given (use -a y to set up as active. -a n to set up as inactive)"
else

	#compile netcode
	cd /home/pi/frosti/netSrc/
	make

	#start frosti_server on bootup
	cd /etc/init.d/
	touch startFrostiServer.sh
	echo "#!/bin/sh" >> startFrostiServer.sh
	echo "/home/pi/frosti/netSrc/frosti_server 8001" >> startFrostiServer.sh
	chmod +x frosti_server.sh
	update-rc.d startFrostiServer.sh defaults

	#set cron jobs
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

	#set timezone
	echo "America/Vancouver" > /etc/timezone
