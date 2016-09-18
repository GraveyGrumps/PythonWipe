#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
import PythonWipe1
class App(Frame):
    file = ''
    def __init__(self,parent):
        Frame.__init__(self,parent)

        self.parent = parent
        self.initUI()

    def fixtime(self,t):
        l = t.split("-")
        print(i for i in l)
        return ''.join([l[0], " Years, ", l[1], " Months, ", l[2], " Days"])
    
    def ListerIzer(self):
        num = 1
        f = open("Locations.txt")
        r = f.readline().rstrip()
        dirList = Listbox(self,width = 100)
        timList = Listbox(self,width = 50)
        while(r != ''):
            dirList.insert(num, r)
            r = f.readline().rstrip()
            timList.insert(num,self.fixtime(r))
            num = num + 1
            r = f.readline().rstrip()
        f.close()
        dirList.grid(row =1, column = 2, rowspan = 3)
        timList.grid(row =1, column = 3, rowspan = 3)


    def initUI(self):
        self.parent.title("PythonWipe")
        self.pack(fill=BOTH, expand = True)

        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 1)
        self.columnconfigure(0, pad = 7)
        self.columnconfigure(1, pad = 7)
        
        addNewBtn = Button(self,text = "Add New Directory", width = 20, command = combine_funcs(self.AddNewWin,self.ListerIzer))
        addNewBtn.grid(row=1,column=0)

        runBtn = Button(self,text = "RUN", width = 20, command = combine_funcs(PythonWipe1.main,self.ListerIzer))
        runBtn.grid(row=1,column=1, padx = 10)

        rmDirBtn = Button(self,text = "Remove Directory", width = 20 ,command = combine_funcs(self.RmDirWin,self.ListerIzer))
        rmDirBtn.grid(row=2,column=0, pady = 10)

        chDelTimBtn = Button(self,text = "Change Deletion Time", width = 20)
        chDelTimBtn.grid(row=2,column=1)

        quitBtn = Button(self,text = "Quit", width = 20, command = self.parent.destroy)
        quitBtn.grid(row=3,column=0,columnspan = 2)

        dirLab = Label(self,text ="File Path")
        dirLab.grid(row=0,column =2)

        delTim = Label(self,text ="Deletion Time")
        delTim.grid(row=0,column = 3)
        self.ListerIzer()

    def AddNewWin(self):
        t = Toplevel(self)
        t.wm_title("Add New Directory")
        App.file = filedialog.askdirectory(initialdir = "C:/")
        if App.file == "":
            t.destroy()
        year = StringVar()
        month = StringVar()
        day = StringVar()
        year.set("00")
        month.set("00")
        day.set("00")
        self.drawDirLabel(t)
        
        expLabel = Label(t,text = "In what time frame would you like this directory's contents deleted")
        yrLabel = Label(t,text ="Years (YY)")
        moLabel = Label(t,text ="Months (MM)")
        dayLabel = Label(t,text="Days (DD)")
        
        savBut = Button(t,text="Save", command = lambda: self.savDir(t,year,month,day))
        chDirBut = Button(t,text="Change Directory",command = lambda: self.getfile(t))
        canBut = Button(t,text="Cancel", command = t.destroy)
        
        yrEnt = Entry(t,textvariable = year)
        moEnt = Entry(t,textvariable = month)
        dayEnt = Entry(t,textvariable = day)
        
        yrLabel.grid(row=2,column=0)
        moLabel.grid(row=2,column=1)
        dayLabel.grid(row=2,column=2)
        yrEnt.grid(row=3,column=0)
        moEnt.grid(row=3,column=1)
        dayEnt.grid(row=3,column=2)
        savBut.grid(row=4,column=0)
        chDirBut.grid(row=4,column=1)
        canBut.grid(row=4,column=2)
        expLabel.grid(row=1,column=0,columnspan=3)

    def savDir(self,t,year,month,day):
        if len(year.get()) > 3:
            self.MakeWarn(1)
            return
        if len(month.get()) > 4:
            self.MakeWarn(2)
            return
        if len(day.get()) > 5:
            self.MakeWarn(3)
            return
        try:
            int(year.get())
            int(month.get())
            int(day.get())
        except ValueError:
            self.MakeWarn(4)
            return
        f = open("Locations.txt",'a')
        f.write(App.file)
        f.write("\n")
        f.write(year.get())
        f.write("-")
        f.write(month.get())
        f.write("-")
        f.write(day.get())
        f.write("\n")
        f.close()
        t.destroy()
        self.ListerIzer()
        
    def MakeWarn(self, var):
        H = Toplevel(self)
        H.wm_title("You Dun Goof'd")
        exitBut = Button(H, text = "I Understand", command = H.destroy)
        exitBut.grid(row=1,column=0)
        if var == 1:
            Label(H, text = "Year can't be longer than 3 digits").grid(row=0,column=0)
        if var == 2:
            Label(H, text = "Month can't be longer than 4 digits").grid(row=0,column=0)
        if var == 3:
            Label(H, text = "Day can't be longer than 5 digits").grid(row=0,column=0)
        if var == 4:
            Label(H, text = "Values Must be Numbers").grid(row=0,column=0)

            
    def drawDirLabel(self,t):
        dirLabel = Label(t,text = ''.join(["Directory Path: ", App.file]))
        dirLabel.grid(row=0,column=0,columnspan=3)
        
    def getfile(self,t):
        file = filedialog.askdirectory(initialdir = "C:/")
        if file != '':
            App.file = file
            self.drawDirLabel(t)
                      
        
    def RmDirWin(self):
        cb =[]
        t = Toplevel(self)
        t.wm_title("Remove Directory")
        howdy = Label(t, text = "Check All Directories That You Would Like To Remove")
        howdy.grid(row = 0, column = 0, columnspan = 2)
        doIt = Button(t, text = "Delete Choices", width = 10, command = lambda:RemoveCheckList(self, t,cb))
        doIt.grid(row = 1, column = 0,)
        noO = Button(t, text = "Cancel", width = 10,  command =t.destroy)
        noO.grid(row = 2, column = 0)
        cb = self.CheckerIzer(t,cb)
    def CheckerIzer(self,t,cb):
        cb = []
        num = 1
        f = open("Locations.txt")
        r = f.readline().rstrip()
        while(r != ''):
            cb.append(IntVar())
            Checkbutton(t, text = r, variable = cb[num-1]).grid(row = num, column = 1,sticky = W) 
            num = num + 1
            f.readline()
            r = f.readline().rstrip()
        f.close()
        return cb

    def Die(self,t):
        self.ListerIzer()
        t.destroy()
            
def RemoveCheckList(a,t,l):
    f = open("Locations.txt",'r')
    fullList = []
    r = f.readline().rstrip()
    while(r != ''):
        fullList.append(r)
        r = f.readline().rstrip()
    f.close()
    f = open("Locations.txt",'w')
    location = 0
    for item in l:
        print(item.get())
        if item.get() == 0:
            f.write(fullList[location])
            f.write("\n")
            location = location + 1
            f.write(fullList[location])
            f.write("\n")
            location = location + 1
        else:
            location = location + 2
    f.close()
    a.Die(t)
        
def main():
  
    root = Tk()
    root.geometry("1000x200+300+300")
    appa = App(root)
    root.mainloop()  


def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

if __name__ == '__main__':
    main()  
