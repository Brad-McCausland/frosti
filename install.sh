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
