import os
import datetime
numdelete = 0
def main():
    global numdelete
    initlog()
    klist = []
    f = open('Locations.txt','r')
    loc= f.readline().rstrip()
    while(loc != ''):
        try:
            os.rmdir(loc)
            modlog([4,loc])
            modlog([5,loc])
        except OSError:
            t = f.readline()
            limit = ParseTime(t)
            modlog([1,loc,limit])
            try:
                OpenDir(loc,limit)
                try:
                    os.rmdir(loc)
                    modlog([4,loc])
                    modlog([5,loc])
                except OSError:
                    modlog([3,loc,limit])
                    klist.extend((loc, t))
            except FileNotFoundError:
                modlog([5,loc])
            loc = f.readline().rstrip()
    f.close()
    EditLocations(klist)

def initlog():
    f = open('log.txt','a+')
    f.write("Log Entry for: ")
    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    f.write("\n")
    f.close()

def modlog(data):
    global numdelete
    f = open('log.txt','a')
    if data[0] == 1:
        f.write("Checking: ")
        f.write(data[1])
        f.write("      Time Limit: ")
        f.write(datetime.datetime.fromtimestamp(data[2]).strftime('%Y-%m-%d'))
        f.write("\n")
        f.close()
    elif data[0] == 2:
        f.write("DELFIL: ")
        f.write(data[1])
        f.write("      File Time: ")
        f.write(datetime.datetime.fromtimestamp(data[2]).strftime('%Y-%m-%d'))
        f.write("\n")
        f.close()
    elif data[0] == 3:
        f.write("From: ")
        f.write(data[1])
        f.write(" ")
        f.write(str(numdelete))
        f.write(" where deleted for being older than: ")
        f.write(datetime.datetime.fromtimestamp(data[2]).strftime('%Y-%m-%d'))
        f.write("\n")
        numdelete = 0
        f.close()
    elif data[0] == 4:
        f.write("DELDIR: ")
        f.write(data[1])
        f.write(" Directory was empty\n")
        f.close()
    elif data[0] == 5:
        f.write("REMOVED FROM LIST OF WATCHED DIRECTORIES: ")
        f.write(data[1])
        f.write(" NO LONGER EXISTS\n")
        f.close()
        
def OpenDir(location,limit):
    global numdelete
    for item in os.listdir(location):
        if os.path.isdir(os.path.join(location,item)) == True:
            #print(item + " Is a directory")
            try:
                os.rmdir(os.path.join(location,item))
                modlog([4,os.path.join(location,item)])
            except OSError:
                OpenDir(os.path.join(location,item),limit)
                try:
                    os.rmdir(os.path.join(location,item))
                    modlog([4,os.path.join(location,item)])
                except OSError:
                    pass
        else:
            #print(item + " Is a file")
            modtime = os.path.getmtime(os.path.join(location,item))
            if not CheckTime(limit,modtime):
                numdelete = numdelete + 1
                DeleteFile(os.path.join(location,item),modtime)
    
def CheckTime(limit,modtime):
    #if limit < time of file
    #keep
    #else
    #Record file path and delete file
    if limit < modtime:
        return True
    else:
        return False
    
    
def ParseTime(limit):
    l = [int(i) for i in limit.split("-")]
    dateHolder = [int(i) for i in datetime.date.today().strftime('%Y-%m-%d').split("-")]
    #Get change time and do math to go back from current time to desired change time then run that through convertime and return that result
    dateHolder[0] = dateHolder[0] - l[0]
    dateHolder[1] = dateHolder[1] - l[1]
    dateHolder[2] = dateHolder[2] - l[2]
    while( dateHolder[1] <= 0):
        dateHolder[0] = dateHolder[0] - 1
        dateHolder[1] = dateHolder[1] + 12
    while( dateHolder[2] <= 0):
        dateHolder[2] = dateHolder[2] + IHateTheCalendar(dateHolder[1], dateHolder[0])
    print("The time limit is ", l[0] , " years:", l[1], " months:", l[2], " days which makes the deletion date:",dateHolder[0], ":",dateHolder[1],":",dateHolder[2])
    return datetime.datetime(dateHolder[0],dateHolder[1],dateHolder[2]).timestamp()

def IHateTheCalendar(month, year):
    if (month == 1) or (month == 3) or (month == 5) or (month == 7) or (month == 8) or (month == 10) or (month == 12):
        return 31
    elif (month == 2) and (year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0)):
        return 29
    elif (month == 2):
        return 28
    else:
        return 30
    
def DeleteFile(location,modtime):
    modlog([2,location,modtime])
    os.remove(location)
    
def EditLocations(klist):
    f = open('Locations.txt','w')
    for item in klist:
        f.write(item)
        f.write("\n")
