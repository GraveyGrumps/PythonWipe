import datetime

def time(t):
    l = [int(i) for i in t.split("-")]
    a = datetime.datetime(l[0],l[1],l[2]).timestamp()
    print(a)
    print (type(datetime.date.today()))
    l = [int(i) for i in datetime.date.today().strftime('%Y-%m-%d').split("-")]
    b = str(l[0]) + "-" + str(l[1]) + "-" str(l[2])
    print(b)

def IHateTheCalendar(month, year):
    if (month == 1) or (month == 3) or (month == 5) or (month == 7) or (month == 8) or (month == 10) or (month == 12):
        return 31
    elif (month == 2) and (year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0)):
        return 29
    elif (month == 2):
        return 28
    else:
        return 30
