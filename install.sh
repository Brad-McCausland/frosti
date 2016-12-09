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

#start frosti web portal on bootup
cd /etc/init.d/
touch startFrostiWeb.sh
echo "#!/bin/sh" >> startFrostiWeb.sh
echo "python /home/pi/frosti/flask/hello.py" >> startFrostiWeb.sh
chmod +x startFrostiWeb.sh
update-rc.d startFrostiWeb.sh defaults

#set timezone
sudo cp /usr/share/zoneinfo/America/Vancouver /etc/localtime

#install pip
sudo apt-get install python-pip
sudo apt-get install python3-pip

#install pip3 and flask for web portal
sudo pip3 install flask
sudo pip3 install flask_login

#additional dependancies
sudo pip install twilio
sudo apt-get install mailutils
sudo apt-get install ssmtp
sudo apt-get install ftp
sudo apt-get install vsftpd

#configure ssmtp
sudo echo "#" > /etc/ssmtp/ssmtp.conf
sudo echo "# Config file for sSMTP sendmail" >> /etc/ssmtp/ssmtp.conf
sudo echo "#" >> /etc/ssmtp/ssmtp.conf
sudo echo "# The person who gets all mail for userids < 1000" >> /etc/ssmtp/ssmtp.conf
sudo echo "# Make this empty to disable rewriting." >> /etc/ssmtp/ssmtp.conf
sudo echo "root=frosti.wwu@gmail.com" >> /etc/ssmtp/ssmtp.conf

sudo echo "# The place where the mail goes. The actual machine name is required no " >> /etc/ssmtp/ssmtp.conf
sudo echo "# MX records are consulted. Commonly mailhosts are named mail.domain.com" >> /etc/ssmtp/ssmtp.conf
sudo echo "mailhub=smtp.gmail.com:587" >> /etc/ssmtp/ssmtp.conf

sudo echo "# Where will the mail seem to come from?" >> /etc/ssmtp/ssmtp.conf
sudo echo "rewriteDomain=" >> /etc/ssmtp/ssmtp.conf

sudo echo "# The full hostname" >> /etc/ssmtp/ssmtp.conf
sudo echo "hostname=raspberrypi" >> /etc/ssmtp/ssmtp.conf

sudo echo "# Are users allowed to set their own From: address?" >> /etc/ssmtp/ssmtp.conf
sudo echo " YES - Allow the user to specify their own From: address" >> /etc/ssmtp/ssmtp.conf
sudo echo " NO - Use the system generated From: address" >> /etc/ssmtp/ssmtp.conf
sudo echo "FromLineOverride=YES" >> /etc/ssmtp/ssmtp.conf
sudo echo "AuthUser=frosti.wwu@gmail.com" >> /etc/ssmtp/ssmtp.conf
sudo echo "AuthPass=frosti492" >> /etc/ssmtp/ssmtp.conf
sudo echo "UseTLS=Yes" >> /etc/ssmtp/ssmtp.conf
sudo echo "UseSTARTTLS=Yes" >> /etc/ssmtp/ssmtp.conf
sudo echo "AuthLogin=Yes" >> /etc/ssmtp/ssmtp.conf

