#This script is given the ip of its counterpart pi
#and downloads its user registers. This is to keep
#users syncronized across both systems, and should
#only be run on the pi that is NOT running the web
#portal.

#!/bin/bash
HOST=$1
USER=pi
PASSWORD=Frosti492

cd /home/pi/frosti/alertSrc/user_register/
ftp -inv $HOST <<EOF
user $USER $PASSWORD
cd /home/pi/frosti/alertSrc/user_register/
get email.txt
get phone.txt
bye
EOF
