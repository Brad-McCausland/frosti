#!/bin bash

#part one of installer. Must be run with sud0

#compile netcode
cd /home/pi/frosti/netSrc/
make

#start frosti_server on bootup
cd /etc/init.d/
touch startFrostiServer.sh
echo "#!/bin/sh" >> startFrostiServer.sh
echo "/home/pi/frosti/netSrc/frosti_server 8001" >> startFrostiServer.sh
chmod +x startFrostiServer.sh
update-rc.d startFrostiServer.sh defaults

#set timezone
sudo echo "America/Vancouver" > /etc/timezone
