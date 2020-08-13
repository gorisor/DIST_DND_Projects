# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 12:31:17 2020

@author: GORISOR
"""

import lib_RandomCharacterGenerator as RCG
import tkinter as tk
from tkinter import filedialog
import os
from functools import partial

# Scrollable frame from: Jose Salvatierra - https://blog.tecladocode.com/tkinter-scrollable-frames/
# Notes: When using, must add widget to self.container
# (e.g. -- tk.Label(frame.scrollable_frame, text="Sample scrolling label").pack() --)
# MouseWheel control added to original function
class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):        
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        # re-size "window" on scroll
        self.scrollable_frame.bind("<Configure>",lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all") ) )
        
        """ WINDOWS ONLY LINE - REMOVE/MODIFY FOR OTHER OSs """
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    # Move up or down on mousewheel control (Windows ONLY)
    """ WINDOWS ONLY FUNCTION - REMOVE/MODIFY FOR OTHER OSs """
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")        


# Import Enemy file from text in neighbor folder /Enemies/
# Will create folder if it doesn't already exist
# See end of file for example enemy layout
def openFileEnemy():
    global battleManager
    path = os.getcwd()
    path += "/Enemies/"
    if not os.path.exists(path):
        os.makedirs(path)
    fileName =  filedialog.askopenfilename(initialdir = path,title = "Select Enemy File",filetypes = (("text files","*.txt"),("all files","*.*")))
    if fileName != "":
        battleManager.importEnemy(fileName)

# Import Player Characters from text file in neighbor folder /Parties/
# Will create folder if it doesn't already exist
# See end of file for example enemy layout
def openFile(t1):
    global battleManager
    path = os.getcwd()
    path += "/Parties/"
    if not os.path.exists(path):
        os.makedirs(path)
    fileName =  filedialog.askopenfilename(initialdir = path,title = "Select Character File",filetypes = (("text files","*.txt"),("all files","*.*")))
    if fileName != "":
        battleManager.importParty(fileName)
        updateMain(t1)
    

# Save party to a text file
# Will create folder if it does not exist
def saveFile():
    global battleManager
    path = os.getcwd()
    path += "/Parties/"
    if not os.path.exists(path):
        os.makedirs(path)
    fileName =  filedialog.asksaveasfile(mode = "w", initialdir = path,defaultextension = ".txt",title = "Select Save Location",filetypes = (("text files","*.txt"),("all files","*.*")))
    if fileName != None:
        battleManager.exportParty(fileName.name)

# Add character through text boxes in program
# All text boxes must be filled in
# ALL numeric values must be numbers
def addCharacter(t1,newChar = None):
    newWindow = tk.Tk()
    # newWindow.iconbitmap("Dodo.ico") # This line breaks the .exe
    newWindow.wm_attributes("-topmost",1)
    newWindow.title("New Character")
    labels = ["Player Name: ","Character Name: ","Class: ","Level: ","STR: ",
              "DEX: ","CON: ","INT: ","WIS: ","CHA: ","ACMod: ","INIT: ","Perception:"]
    le = []
    ee = []        
    # Loop through the input and text boxes
    for i in range(len(labels)):
        lt = tk.Label(master = newWindow,text = labels[i])
        et = tk.Entry(master = newWindow, width=50)
        le.append(lt)
        ee.append(et)
        le[i].grid(row=i, column=0, sticky="e")
        ee[i].grid(row=i, column=1, sticky="w")
        if newChar != None:
            ee[i].insert(0,newChar[i])
    
    checkAddwVals = partial(checkAdd, ee,t1)
    clearValueswVals = partial(clearValues, ee)
    rollStatswVals = partial(rollStats2,ee)    
    # Control buttons
    b0 = tk.Button(master = newWindow,text = "Roll Stats",command = rollStatswVals,bg = "light goldenrod")
    b1 = tk.Button(master = newWindow,text = "Add Character",command = checkAddwVals)
    b2 = tk.Button(master = newWindow,text = "Clear Values",command = clearValueswVals)
    b3 = tk.Button(master = newWindow,text = "Exit",command = newWindow.destroy,bg="pink1")
    b0.grid(row = i + 1, column = 0)
    b1.grid(row = i + 1, column = 1,sticky = "w")
    b2.grid(row = i + 1, column = 1)
    b3.grid(row = i + 1, column = 1,sticky = "e")

# Helper Function to addCharacter
# Will fill the 6 attributes with 4d6 choose 3
def rollStats2(ee):
    stats = RCG.rollStats()
    for i in range(4,10):
        ee[i].delete(0, len(ee[i].get()))
        ee[i].insert(0,stats[i-4])

# Helper function for incorrect input
# Displays message in a red pop-up window
def makeErrorWindow(message):
    errorWindow = tk.Tk()
    # errorWindow.iconbitmap("Dodo.ico") # This line breaks the .exe
    errorWindow.wm_attributes("-topmost",1)
    errorWindow.title("ERROR!")
    l1 = tk.Label(master = errorWindow,text = message,bg = "pink1")
    l1.pack()

# Helper function for correct input
# Displays message in a yellow pop-up window
def makeSuccessWindow(message):
    successWindow = tk.Tk()
    # successWindow.iconbitmap("Dodo.ico") # This line breaks the .exe
    successWindow.wm_attributes("-topmost",1)
    successWindow.title("SUCCESS!")
    l1 = tk.Label(master = successWindow,text = message,bg = "lightgoldenrod")
    l1.pack()

# Helper function for addCharacter
# Test values from entry to ensure correct values the create Character
def checkAdd(ee,t1):
    global battleManager
    charInfo = []
    for i in range(13):
        charInfo.append(ee[i].get())
        if charInfo[i] == "":
            makeErrorWindow("The charater could not be created. Please fill all values and try again.")
            return
    for i in range(3,13):
        try:
            charInfo[i] = int(charInfo[i])
        except:
            makeErrorWindow("The charater could not be created. Please check values and try again.")
            return
    newCharacter = RCG.playerCharacter(charInfo)
    battleManager.addPlayerCharacter(newCharacter)
    updateMain(t1)
    makeSuccessWindow("The character was successfully added.")

# Helper Function for addCharacter
# Clears all entry values
def clearValues(ee):
    for i in range(len(ee)):
        ee[i].delete(0, len(ee[i].get()))

# Removes all party members from list
def clearParty(t1):
    global battleManager
    battleManager.clearParty()
    updateMain(t1)

# Class for connecting buttons to specific characters
# packs them together
class charControl:
    def __init__(self,i,fi,combatant,window):
        COLORS = ("gray85","gray75")
        self.f = tk.Frame(master = fi.scrollable_frame,bg = COLORS[i%2])
        self.t = tk.Text(master = self.f,bg = COLORS[i%2],relief="flat",width=33,height=6)
        self.t.delete("1.0","end")
        self.t.insert("end",combatant.fastPrint())
        self.e = tk.Entry(master = self.f,width = 4)
        self.e.insert(0,"0")
        self.name = combatant.name        
        self.b2 = tk.Button(master = self.f,text = "Damage/Heal",command = lambda:[self.damageCombatant(),drawInitWindow(window)])
        self.b = tk.Button(master = self.f,text = "Kill",command = lambda:[self.kill(),drawInitWindow(window)])
        
        self.b.grid(row=0,column=0,columnspan=2,sticky="ew")
        self.e.grid(row=1,column=1)
        self.b2.grid(row=1,column=0)
        self.t.grid(row=0,column=2,rowspan=2,sticky="news")
        
        self.f.pack()
    
    # Update Health of Combatant
    def damageCombatant(self):
        global battleManager
        battleManager.damageCombatant(self.name,self.e)
    
    # Remove combatant from battle
    def kill(self):
        global battleManager
        battleManager.removeCombatant(self.name)

# Helper function to enterCombat
# Creates and draws buttons and characters
def drawInitWindow(initWin):
    # Delete all widgets from window
    for victim in initWin.winfo_children():
        victim.destroy()
    
    # Layout buttons for controlling Init
    combat = battleManager.getINITs()
    f1 = tk.Frame(master=initWin,height = 10,width = 350,bg = "red")
    b1 = tk.Button(master = f1,text = "Forward", command = lambda:[battleManager.nextCombatant(),drawInitWindow(initWin)])
    b2 = tk.Button(master = f1,text = "Backward", command = lambda:[battleManager.lastCombatant(),drawInitWindow(initWin)])
    b1.pack(side = "left",fill = "both",expand = True)
    b2.pack(side = "right",fill = "both",expand = True)
    f1.pack(fill = "both")
    
    # Fill scrollable frame with class charControls
    charControls = []
    f2 = ScrollableFrame(initWin)
    for i in range(len(combat)):
        charControls.append(charControl(i,f2,combat[i][0],initWin))  
    f2.pack(expand = True, fill = tk.BOTH)

# Helper Function for enterCombat
# Displays critical successes and failures for INIT
def critInitWin():
    global battleManager
    info = battleManager.returnCrits()
    
    # Don't make window if no crits
    if info == "":
        return
    critInitWin = tk.Tk()
    critInitWin.title("Critical Initiatives")
    # critInitWin.iconbitmap("Dodo.ico") # This line breaks the .exe
    critInitWin.wm_attributes("-topmost",1)
    critInitWin.minsize(200,100)
    t1 = tk.Label(master = critInitWin, text = info,justify=tk.LEFT, 
                  bg = "gray94",relief="flat")
    t1.pack()
    
# Start combat with party and loaded enemies
def enterCombat():
    global battleManager
    initWin = tk.Tk()
    initWin.title("Initiative")
    # initWin.iconbitmap("Dodo.ico") # This line breaks the .exe
    initWin.wm_attributes("-topmost",1)
    initWin.minsize(400,130)
    initWin.maxsize(400,5000)
    battleManager.startCombat()
    critInitWin()
    drawInitWindow(initWin)

# Add a number of random enemies to enemy pool
def addEnemies(numEnemies):
    global battleManager
    try:
        numEnemies = int(numEnemies)
    except:
        makeErrorWindow("Could not add enemies, incorrect value input.")
        return
    battleManager.addEnemies(numEnemies)

# Class for connecting buttons to specific characters
# packs them together for main screen
class pCharControl:
    def __init__(self,i,fi,combatant,window):
        COLORS = ("gray85","gray75")
        self.f = tk.Frame(master = fi.scrollable_frame,bg = COLORS[i%2],width=150)
        self.t = tk.Text(master = self.f,bg = COLORS[i%2],relief="flat",height=6)
        self.t.delete("1.0","end")
        self.t.insert("end",combatant.fastPrint())        
        self.name = combatant.name
        self.b2 = tk.Button(master = self.f,text = "Remove",command = lambda:[self.removeCh(),updateMain(window)])
        self.b = tk.Button(master = self.f,text = "Edit",command = lambda:[self.edit(window),updateMain(window)])

        self.b.grid(row=0,column=0,sticky="ew")
        self.b2.grid(row=1,column=0,sticky="ew")
        self.t.grid(row=0,column=1,rowspan=2)
        
        self.f.pack()
    
    # Update Health of Combatant
    def removeCh(self):
        global battleManager
        battleManager.removePartyMember(self.name)
    
    # Remove combatant from battle
    def edit(self,t1):
        global battleManager 
        ch = battleManager.getPartyMember(self.name)
        self.removeCh()
        addCharacter(t1,newChar = ch)
        

# Draw the main window
def updateMain(root):
    # Delete all widgets from window
    for victim in root.winfo_children():
        victim.destroy()
    
    global battleManager    
    # Fill scrollable frame with class charControls
    charControls = []
    tk.Grid.rowconfigure(root, 2, weight=1)
    tk.Grid.columnconfigure(root, 4, weight=1)
    f2 = ScrollableFrame(root)
    for i in range(len(battleManager.playerCharacters)):   
        charControls.append(pCharControl(i,f2,battleManager.playerCharacters[i],root))  
    
    e7 = tk.Entry(width = 5)
    b1 = tk.Button(text = "Import Party", command = lambda:[openFile(root)])
    b3 = tk.Button(text = "Export Party", command = saveFile)
    b2 = tk.Button(text = "Add Character", command = lambda:[addCharacter(root)])
    b5 = tk.Button(text = "Clear Party", command = lambda:[clearParty(root)],bg = "pink1")
    b6 = tk.Button(text = "Start Combat", command = enterCombat,bg = "lightgoldenrod",height = 3)
    b8 = tk.Button(text = "Add Enemies->",command = lambda:addEnemies(e7.get()))
    b0 = tk.Button(text = "Import Enemies",command = openFileEnemy)
    b9 = tk.Button(text = "Clear Enemies",command = battleManager.clearEnemies,bg = "pink1")

    # Layout Buttons
    b1.grid(row = 0, column = 0,sticky = "news")
    b2.grid(row = 0, column = 1,sticky = "news")
    b3.grid(row = 0, column = 2,sticky = "news")
    b5.grid(row = 0, column = 3,sticky = "news")
    b6.grid(row = 0, column = 4,rowspan = 2,sticky = "news")    
    b0.grid(row = 1, column = 0,sticky = "news")
    b8.grid(row = 1, column = 1,sticky = "news")
    e7.grid(row = 1, column = 2,sticky = "news")
    e7.insert(0,"10")
    b9.grid(row = 1, column = 3,sticky = "news")
    f2.grid(row = 2, column = 0, columnspan = 5,sticky = "news")
    
# Main Window
root = tk.Tk()
root.title("GORISORs Epic Battle Manager")
# root.iconbitmap("Dodo.ico") # This line breaks the .exe
root.wm_attributes("-topmost",1)
root.minsize(450,55)
root.maxsize(width = 450,height = 5000)
battleManager = RCG.manager()
updateMain(root)
root.mainloop()
    
