from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os
from datetime import *
import calendar
import json

settings = {'logpath' : str(os.path.abspath(os.path.dirname(__file__)))}

def pushF(message = ""):
    global settings
    print("Saving settings.")
    try:
        with open("./conf.json", 'w') as conf:
            json.dump(settings, conf)
        print("Success!")
    except:
        print("Failure!")

def pullF(message = ""):
    global settings
    print("Loading settings...")
    try:
        with open("./conf.json", 'r') as conf:
            settings = json.load(conf)
        print("Success!")
    except FileNotFoundError:
        print("No config file found!")

pullF()

root = Tk()
root.geometry("500x700+300+300")
root.title("Dans' Dumb Chatterino Log Panel")

statusBar = StringVar()
statusBar.set("Enter a username")

dirFrame = Frame(root, borderwidth=2)
logDir = StringVar()
logDir.set(settings['logpath'])

filterDate = date.today()
filterLevel = 0

baseFrame = Frame(root, relief=RAISED, borderwidth=2)

messageList = []
lbVar = StringVar()
lbVar.set('')
lb = Listbox(baseFrame, listvariable=lbVar)

def selectFolder():
    logPath = os.path.dirname(filedialog.askopenfilename(initialdir=logDir, title="Select a Log File in the Correct Folder", filetypes=[('logfile', '*.log')]))
    logDir.set(logPath)
    settings['logpath'] = logPath
    pushF()
    lb.delete(0, 'end')
    # logPath = filedialog.askdirectory(initialdir=logDir, title="Select Log Folder", filetypes=('logfile','*.log'))
    # logDir.set(logPath)
    # settings['logpath'] = logPath
    # pushF()
    # lb.delete(0, 'end')

logDirBtn = Button(dirFrame, text="<<<Select Log Folder", command=selectFolder).pack(side=RIGHT, anchor=N)
logDirLabel = Label(dirFrame, textvariable=logDir).pack(side=RIGHT)

dirFrame.pack(fill=X)


baseFrame.pack(fill=BOTH, padx=2, pady=2, expand=True)

userFrame = Frame(baseFrame)
userFrame.pack(fill=X, padx=2, pady=2)

userNameLabel = Label(userFrame, text="User:").pack(side=LEFT, padx=2, pady=2)
userNameEntry = Entry(userFrame)
userNameEntry.pack(side=LEFT, fill=X, padx=2, pady=2, expand=True)

messageList = []
lbVar = StringVar()
lbVar.set('')
lb = Listbox(baseFrame, listvariable=lbVar)
lb.pack(fill=BOTH, padx=5, pady=3, expand=True)

def search(event=None):
    global filterDate
    global filterLevel
    
    lb.delete(0, 'end')
    
    messageList = []
    searchName = userNameEntry.get()
    if len(searchName) > 0:
        properName = ""
        for log in os.listdir(logDir.get()):
            fileName = os.path.join(logDir.get(), log)
            fileName = os.path.normpath(fileName)
        
            try:
                with open(fileName, encoding="utf-8") as thisLog:
                    logDateStr = (thisLog.name.split('-', 1))[1][:-4]
                    logDate = date.fromisoformat(logDateStr)
                
                    if filterLevel == 3:
                        if logDate == filterDate:
                            for line in thisLog.read().splitlines():
                                if line[0] != '#':
                                    chatter = (line[12:].split(':', 1))[0]
                                    if chatter.lower() == searchName.lower():
                                        properName = chatter
                                        messageList.append(logDateStr + ' ' + line)
                
                    elif filterLevel == 2:
                        if logDate.year == filterDate.year:
                            if logDate.month == filterDate.month:
                                for line in thisLog.read().splitlines():
                                    if line[0] != '#':
                                        chatter = (line[12:].split(':', 1))[0]
                                        if chatter.lower() == searchName.lower():
                                            properName = chatter
                                            messageList.append(logDateStr + ' ' + line)
                
                    elif filterLevel == 1:
                        if logDate.year == filterDate.year:
                            for line in thisLog.read().splitlines():
                                if line[0] != '#':
                                    chatter = (line[12:].split(':', 1))[0]
                                    if chatter.lower() == searchName.lower():
                                        properName = chatter
                                        messageList.append(logDateStr + ' ' + line)
                
                    else:
                        for line in thisLog.read().splitlines():
                            if line[0] != '#':
                                chatter = (line[12:].split(':', 1))[0]
                                if chatter.lower() == searchName.lower():
                                    properName = chatter
                                    messageList.append(logDateStr + ' ' + line)
                            
            except:
                print("Failure!")
    
        if len(messageList) > 0:
            statusBar.set(properName)
            for item in messageList:
                lb.insert(0, item)
        else:
            statusBar.set("No logs found for " + searchName + "!")
    
    else:
        statusBar.set("Enter a username")
    
    lb.pack()

searchBtn = Button(userFrame, text="Search", command=search).pack(side=RIGHT, padx=2, pady=2)
userNameEntry.bind('<Return>', search)

statusBarLabel = Label(baseFrame, textvariable=statusBar).pack(side=LEFT, padx=2, pady=1)

dayChosen = ttk.Combobox(baseFrame, width=3, state='disabled')
daylist = ['All']
for x in range(1, 32):
    daylist.append(x)
dayChosen['values'] = daylist
dayChosen.current(0)

monthChosen = ttk.Combobox(baseFrame, width=10, state='disabled')
monthChosen['values'] = ('All', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
monthChosen.current(0)

yearChosen = ttk.Combobox(baseFrame, width=5, state='readonly')
yearChosen['values'] = ('All', '2021', '2020', '2019', '2018', '2017')
yearChosen.current(0)

def filterConfig():
    global filterLevel
    
    if yearChosen.current() > 0:
        filterLevel = 1
        
        if monthChosen.current() > 0:
            filterLevel = 2
            
            if dayChosen.current() > 0:
                filterLevel = 3
    else:
        filterLevel = 0
        
    #print(filterLevel)

def filter():
    global filterDate
    
    if yearChosen.current() > 0:
        filterDate = filterDate.replace(year=int(yearChosen.get()))
        
    if monthChosen.current() > 0:
        filterDate = filterDate.replace(month=monthChosen.current())
    
    if dayChosen.current() > 0:
        filterDate = filterDate.replace(day=dayChosen.current())
    
    filterConfig()
    search()

filterBtn = Button(baseFrame, text="Filter", command=filter, state='disabled')

def monthChanged(event=None):
    
    if monthChosen.current() > 0:
        dayChosen.configure(state='readonly')
    else:
        dayChosen.current(0)
        dayChosen.configure(state='disabled')
    
    if yearChosen.current() > 0:
        monthChosen.configure(state='readonly')
        filterBtn.configure(state='active')
    else:
        dayChosen.current(0)
        dayChosen.configure(state='disabled')
        monthChosen.current(0)
        monthChosen.configure(state='disabled')
        filterBtn.configure(state='disabled')
    
    if monthChosen.current() > 0 and yearChosen.current() > 0:
        mrange = calendar.monthrange(int(yearChosen.get()), monthChosen.current())[1]
        
        currentDay = dayChosen.current()
        daylist = ['All']
        
        for x in range(1, mrange + 1):
            daylist.append(x)
        
        dayChosen['values'] = daylist
       
        if currentDay > mrange:
            dayChosen.current(mrange)
        else:
            dayChosen.current(currentDay)

monthChosen.bind("<<ComboboxSelected>>", monthChanged)
yearChosen.bind("<<ComboboxSelected>>", monthChanged)

def clear():
    global filterDate
    
    dayChosen.current(0)
    dayChosen.configure(state='disabled')
    monthChosen.current(0)
    monthChosen.configure(state='disabled')
    yearChosen.current(0)
    filterBtn.configure(state='disabled')
    
    filterDate = date.today()
    filterConfig()

clearBtn = Button(baseFrame, text="Clear", command=clear)

clearBtn.pack(side=RIGHT, padx=2, pady=2)
filterBtn.pack(side=RIGHT, padx=2, pady=2)
dayChosen.pack(side=RIGHT, padx=2, pady=2)
monthChosen.pack(side=RIGHT, padx=2, pady=2)
yearChosen.pack(side=RIGHT, padx=2, pady=2)

root.mainloop()

# def main():
    # root = Tk()
    # root.geometry("500x700+300+300")
    # root.title("Jacob's Scuffed Logger")
    # root.mainloop()

# if __name__ == '__main__':
    # main()