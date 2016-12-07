#!/usr/bin/python3

#Logger for FROSTI

import csv
import datetime
import os

#Writes readings 1 2 and 3 to file in logDir.
#CSV files are named with current date y-m-d, timestamps are saved inside file.
filedir = os.path.dirname(os.path.abspath(__file__))
rootdir = filedir[::-1].split('/',1)[1][::-1]

logDir = rootdir + "/logs/"

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
        with open(logDir + date + '.csv', 'a+') as csvfile:
            logWriter = csv.writer(csvfile, delimiter=',')

            if(newfile):
                logWriter.writerow(['Timestamp', 'Freezer1 *C', 'Freezer2 *C', 'Freezer3 *C'])
            logWriter.writerow([datetime.datetime.now().strftime("%H:%M"), temp1, temp2, temp3])

        return 0
    except:
        print("Unable to open file for writing")
        return -1

#returns true if log for yyyy-mm-dd exists
def logExist(logdate):
    if(os.path.exists(logDir + logdate + '.csv')):
        return True
    return False

#Wrapper for getLogs to get a specific day of logs
#returns past day of logs for yyyy-mm-dd if it exists.
def getLogDate(logdate):

    if logdate == 'today':
        offset = 0
    else:
        offset = datetime.datetime.now() - datetime.datetime.strptime(logdate,"%Y-%m-%d")
        offset = offset.days

    #returns 12 logs per whatever hour it is currently.
    n = int(datetime.datetime.now().strftime("%H")) * 12
    if n == 0:
        n += 1

    #override to show last 24 hours or as much as available no matter what
    n = 288

    times = getLogs(n,0,offset)[:-1]
    f1 = getLogs(n,1,offset)[:-1]
    f2 = getLogs(n,2,offset)[:-1]
    f3 = getLogs(n,3,offset)[:-1]
    return times,f1,f2,f3

#returns last (most recent) n temp values of  from freezer F (1 to 3) as array.
# Optional dayOffset to see past days
#Will include data from additional days/csvs if n large enough
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
                tempList.extend(     getLogs(n-len(tempList),f,dayOffset + 1)    )
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
