#!/usr/bin/python

import datetime
import time
import sys

def getUnixTime(currDate, currTime):
    dt = datetime.datetime.strptime(currDate + ' ' + currTime, '%Y-%m-%d %H:%M:%S')
    return time.mktime(dt.timetuple())

def getStrFromUnixTime(unixTime):
    return datetime.datetime.fromtimestamp(unixTime).strftime('%Y-%m-%d %H:%M:%S')

class Session:
    def __init__(self, userIp, startTime):
        self.userIp = userIp
        self.startTime = startTime
        self.endTime = startTime
        self.docCount = 1

    def __str__(self):
        startTimeStr = getStrFromUnixTime(self.startTime)
        endTimeStr = getStrFromUnixTime(self.endTime)
        return "{},{},{},{},{}\n".format(self.userIp,startTimeStr,endTimeStr,self.endTime - self.startTime + 1,self.docCount)

def main():
    inputFilePath = sys.argv[1]
    inactivityPeriodFilePath = sys.argv[2]
    inactivityPeriodFile = open(inactivityPeriodFilePath, 'r')
    outputFilePath = sys.argv[3]
    outputFile = open(outputFilePath, 'w')
    isHeader = True
    userSession = {}    # IP to session mapping
    activeSession = []  # active user sessions

    inactivityPeriod = int(inactivityPeriodFile.read().split('\n')[0])

    with open(inputFilePath) as f_in:
        for line in f_in:
            # skip first line
            if isHeader:
                isHeader = False
                continue

            inputRow = line.split(',')
            currTime = int(getUnixTime(inputRow[1],inputRow[2]))

            # expire older sessions
            sessionsToExpire = []
            for e in activeSession:
                if  currTime - e.endTime > inactivityPeriod:
                    sessionsToExpire.append(e)
                    activeSession.pop(activeSession.index(e))
                    del userSession[e.userIp]
                else:
                    break
            # sorting in the same order to appear as in the input file
            sessionsToExpire = sorted(sessionsToExpire, key = lambda e: e.startTime)
            for e in sessionsToExpire:
                outputFile.write(str(e))

            if inputRow[0] in userSession:
              # update existing active session
              userSessionObj = userSession[inputRow[0]]
              activeSession.pop(activeSession.index(userSessionObj))
              userSessionObj.docCount += 1
              userSessionObj.endTime = currTime
            else:
              # create new session
              userSessionObj = Session(inputRow[0],currTime)
              userSession[inputRow[0]] = userSessionObj
            activeSession.append(userSessionObj)

    # expire all remaining sessions after sorting by start time
    activeSession = sorted(activeSession, key= lambda e: e.startTime)
    for e in activeSession:
        outputFile.write(str(e))

if __name__ == "__main__": main()
