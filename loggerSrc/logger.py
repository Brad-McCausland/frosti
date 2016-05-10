#!/usr/bin/python3.4

import csv
import datetime
import os

#24 hour style
#print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
#12 hour style
#blam = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")


def log(logDir,temp1,temp2,temp3):
    newfile = True
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    if(os.path.exists(logDir + date + '.csv')):
        newfile = False
    else:
        #moved this here because we dont need to check for directory again if we already know todays file exists
        if(not os.path.exists(logDir)):
           try:
               os.makedirs(logDir)
           except:
               print("Log directory does not exist and unable to create it")
               raise
        
    with open(logDir + date + '.csv', 'a', newline='') as csvfile:
        logWriter = csv.writer(csvfile, delimiter=',')
        
        if(newfile):
            logWriter.writerow(['Timestamp', 'Freezer1 *C', 'Freezer2 *C', 'Freezer3 *C'])
        logWriter.writerow([datetime.datetime.now().strftime("%H:%M"), temp1, temp2, temp3])


def cleanLogs(logDir):
    SevenDays = datetime.timedelta(days = 7)
    logs = os.listdir(logDir)

    for log in logs:
        try:
            if(datetime.datetime.now() - datetime.datetime.strptime(log,"%Y-%m-%d.csv") > SevenDays):
                os.remove(logDir + log)
        except:
            pass

testdirectory = "/home/pi/frosti/logs/"         
log(testdirectory,30,40,50)
cleanLogs(testdirectory)


