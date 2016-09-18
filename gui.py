#! /usr/bin/python
#! 
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
        
        addNewBtn = Button(self,text = "Add New Directory", width = 22, command = combine_funcs(self.AddNewWin,self.ListerIzer))
        addNewBtn.grid(row=1,column=0)

        runBtn = Button(self,text = "RUN", width = 22, command = combine_funcs(PythonWipe1.main,self.ListerIzer))
        runBtn.grid(row=1,column=1, padx = 10)

        rmDirBtn = Button(self,text = "Remove Directory", width = 22 ,command = combine_funcs(self.RmDirWin,self.ListerIzer))
        rmDirBtn.grid(row=2,column=0, pady = 10)

        chDelTimBtn = Button(self,text = "Change Deletion TimeFrame", width = 22, command = combine_funcs(self.ChDelTimWin,self.ListerIzer))
        chDelTimBtn.grid(row=2,column=1)

        quitBtn = Button(self,text = "Quit", width = 22, command = self.parent.destroy)
        quitBtn.grid(row=3,column=0,columnspan = 2)

        dirLab = Label(self,text ="File Path")
        dirLab.grid(row=0,column =2)

        delTim = Label(self,text ="Deletion Time")
        delTim.grid(row=0,column = 3)
        self.ListerIzer()
    
    def ChDelTimWin(self):
        t = Toplevel(self)
        t.wm_title("Change Directory Deletion TimeFrame")
        title = Label(t,text="Select Directory from List to change Deletion TimeFrame")
        dirLabel = Label(t,text ="Directory Paths")
        timLabel = Label(t,text ="Current TimeFrame")
        
        editBut = Button(t,text = "Change", width = 10,command = lambda: self.change(t,dirBox))
        exitBut = Button(t,text = "Close", width=10, command = t.destroy)
        dirBox, timBox = self.ChTimListerIzer(t)
        timBox.configure(state=DISABLED)                                                                  
        dirBox.grid(row =2, column = 0, rowspan = 2,columnspan = 2)
        timBox.grid(row =2, column = 3, rowspan = 2,columnspan = 2)
        title.grid(row=0,column=0,columnspan=5)
        dirLabel.grid(row=1,column=0,columnspan=2)
        timLabel.grid(row=1,column=3,columnspan=2)
        editBut.grid(row=5,column = 0)
        exitBut.grid(row=5,column=2)
        
    def ChTimListerIzer(self,t):
        dirBox = Listbox(t,width = 100)
        timBox = Listbox(t,width = 50)
        f = open("Locations.txt")
        r = f.readline().rstrip()
        num = 0
        while(r != ''):
            dirBox.insert(num, r)
            r = f.readline().rstrip()
            timBox.insert(num,self.fixtime(r))
            num = num + 1
            r = f.readline().rstrip()
        f.close()
        return dirBox, timBox
    
    def change(self,window,listBox):
        try:
            selection = listBox.get(listBox.curselection())
        except TclError:
            return
        H = Toplevel(window)
        year = StringVar()
        month = StringVar()
        day = StringVar()
        yr,mo,da = self.GetYrMoDa(selection)
        print (yr,mo,da)
        year.set(yr)
        month.set(mo)
        day.set(da)
        
        dirLabel = Label(H,text = selection,)
        saveBut = Button(H,text = "Save Changes", width = 20, command = lambda: self.ChangeDirTime(window,H,selection,year,month,day))
        closeBut = Button(H,text="Close", width = 20,command = H.destroy)
        self.DaterIzer(H,year,month,day)
    
        dirLabel.grid(row=0,column=0,columnspan=3)
        saveBut.grid(row=4,column=0)
        closeBut.grid(row=4,column=2)

    def ChangeDirTime(self,window,H,loc,year,month,day):
        if(self.WarningChecker(H,year,month,day)):
            dat = ''.join([year.get(),'-',month.get(),'-',day.get()])
            l = []
            f = open("Locations.txt",'r')
            a = f.readline().rstrip()
            while(a != ''):
                l.append(a)
                a = f.readline().rstrip()
            f.close()
            f = open("Locations.txt",'w')
            skip = False
            for items in l:
                if skip == True:
                    f.write(dat)
                    f.write("\n")
                    skip = False
                    continue
                if items != loc:
                    f.write(items)
                    f.write("\n")
                else:
                    skip = True
                    f.write(items)
                    f.write("\n")
            f.close()
            window.destroy()
            H.destroy()
            self.ChDelTimWin()
        
        
    def GetYrMoDa(self,dirName):
        f = open("Locations.txt",'r')
        a = f.readline().rstrip()
        while(a != dirName):
            print (dirName)
            print(a)
            a=f.readline().rstrip()
            
        l = f.readline().rstrip().split('-')
        f.close()
        return l
    
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
        self.DaterIzer(t,year,month,day)
        savBut = Button(t,text="Save", command = lambda: self.savDir(t,year,month,day))
        chDirBut = Button(t,text="Change Directory",command = lambda: self.getfile(t))
        canBut = Button(t,text="Cancel", command = t.destroy)
        
        
        savBut.grid(row=4,column=0)
        chDirBut.grid(row=4,column=1)
        canBut.grid(row=4,column=2)
        
        
    def DaterIzer(self,t,year,month,day):
        
        expLabel = Label(t,text = "In what time frame would you like this directory's contents deleted")
        yrLabel = Label(t,text ="Years (YY)")
        moLabel = Label(t,text ="Months (MM)")
        dayLabel = Label(t,text="Days (DD)")
        yrEnt = Entry(t,textvariable = year)
        moEnt = Entry(t,textvariable = month)
        dayEnt = Entry(t,textvariable = day)
        yrLabel.grid(row=2,column=0)
        moLabel.grid(row=2,column=1)
        dayLabel.grid(row=2,column=2)
        yrEnt.grid(row=3,column=0)
        moEnt.grid(row=3,column=1)
        dayEnt.grid(row=3,column=2)
        expLabel.grid(row=1,column=0,columnspan=3)

    def WarningChecker(self,t,year,month,day):
        if len(year.get()) > 3:
            self.MakeWarn(1,t)
            return 0
        if len(month.get()) > 4:
            self.MakeWarn(2,t)
            return 0
        if len(day.get()) > 5:
            self.MakeWarn(3,t)
            return 0
        try:
            int(year.get())
            int(month.get())
            int(day.get())
        except ValueError:
            self.MakeWarn(4,t)
            return 0
        return 1
        
    def savDir(self,t,year,month,day):
        if(self.WarningChecker(t,year,month,day)):
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
        
    def MakeWarn(self, t, var):
        H = Toplevel(t)
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
