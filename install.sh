#!/bin bash

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
echo "*/5 * * * * python /home/pi/frosti/testDriver.py" >> mycron
echo "*/15 * * * * /home/pi/frosti/netSrc/frosti_client 127.0.0.1 8001" >> mycron
crontab mycron
rm mycron

#set timezone
echo "America/Vancouver" > /etc/timezone
