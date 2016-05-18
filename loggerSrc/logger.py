#!/usr/bin/python3.4

#Logger for FROSTI

import csv
import datetime
import os

#Writes readings 1 2 and 3 to file in logDir.
#CSV files are named with current date y-m-d, timestamps are saved inside file.

logDir = "/home/pi/frosti/logs/"

#logDir requires trailing slash
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
               return -1

    try:
        with open(logDir + date + '.csv', 'a', newline='') as csvfile:
            logWriter = csv.writer(csvfile, delimiter=',')
            
            if(newfile):
                logWriter.writerow(['Timestamp', 'Freezer1 *C', 'Freezer2 *C', 'Freezer3 *C'])
            logWriter.writerow([datetime.datetime.now().strftime("%H:%M"), temp1, temp2, temp3])
            
        return 0
    except:
        print("Unable to open file for writing")
        return -1
        


#returns last n temp values of freezer F (1 to 3) as array
#returns False boolean on error. 'False' will be last value in list if n is greater than all available logs
def getLogs(n,f,dayOffset):
    date = datetime.datetime.today() - datetime.timedelta(days = dayOffset)
    date = date.strftime("%Y-%m-%d")
    tempList = []

    #If file does not exist, its probably 12:01am or something so lets check yesterday
    if(not os.path.exists(logDir + date + '.csv')):
        date = datetime.datetime.today() - datetime.timedelta(days = 1 + dayOffset)
        date = date.strftime("%Y-%m-%d")

    if(os.path.exists(logDir + date + '.csv')):
        with open(logDir + date + '.csv', 'r', newline='') as csvfile:
            logReader = csv.reader(csvfile, delimiter=',')
            next(logReader,None)
            
            for row in logReader:
                tempList.append(row[f])
            tempList.reverse()

            if len(tempList) < n:
                tempList.extend(getLogs(logDir,n-len(tempList),f,dayOffset + 1))
                return tempList

            else:
                return tempList[:n]
            
    else:
        return [False] 


#removes week+ old logs
def cleanLogs(logDir):
    maxAge = datetime.timedelta(days = 1825)
    logs = os.listdir(logDir)

    for log in logs:
        try:
            if(datetime.datetime.now() - datetime.datetime.strptime(log,"%Y-%m-%d.csv") > maxAge):
                os.remove(logDir + log)
        except:
            pass

#24 hour style
#print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
#12 hour style
#datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
        
#testdirectory = "C:\\Users\\Avery\\Desktop\\frosti\\logs\\"                  
#b = logg(0,50)
#print(b)
#print( getLogs(testdirectory,15,1,0) )

#cleanLogs(testdirectory)
