import os
import datetime
import time
def main():
    f = open('Locations.txt','r')
    loc= f.readline().rstrip()
    while(loc != ''):
        limit = f.readline()
        limit = ParseTime(time)
        OpenDir(loc,time)
        loc = f.readline()

def OpenDir(location,limit):
    for item in os.listdir(location):
        if os.path.isdir(os.path.join(location,item)) == True:
            print(item + " Is a directory")
            OpenDir(os.path.join(location,item),limit)
        else:
            print(item + " Is a file")
            print(os.path.getmtime(os.path.join(location,item)))
            print(datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(location,item))).strftime('%Y-%m-%d %H:%M:%S'))
    
def CheckTime(limit):    
    #if limit < time of file
    #keep
    #else
    #Record file path and delete file

def ConvertTime(limit):
    l = [int(i) for i in limit.split("-")]
    return datetime.datetime(l[0],l[1],l[2]).timestamp()
    
    
def ParseTime(limit):
    #Get change time and do math to go back from current time to desired change time then run that through convertime and return that result
    limit = limit
