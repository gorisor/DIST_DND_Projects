# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 19:36:29 2020

@author: GORISOR
"""
import random
import tkinter as tk

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

# Roll dice (Num is number of dice, d is number of sides, mod is single addition modifier)
def rolld(num,d,mod):
    value = mod
    for i in range(num):
        value += random.randint(1,d)
    return value

# Add dice roll to output
# val is sides of die, hist is string to update
def diceWindow(val,hist):
    global windows
    if type(val) != int:
        try:
            val = int(val)
            if val <= 0:
                return
        except:
            return
    roll = rolld(1,val,0)
    message = "1d" + str(val) + " = " + str(roll) + "\n" + hist.get()
    hist.set(message)

# Create dice buttons (d4-d100)
def makeButton(i,values,labels,f1,hist):
    tk.Button(master=f1,text=labels[i],font=fontB,command=lambda:diceWindow(values[i],hist)).grid(row=i+1,column=0,columnspan=2,sticky="news")

# Main window function
def updateMain(root):
    # Set up frames
    f1 = tk.Frame(master=root)
    f0 = ScrollableFrame(f1)
    hist = tk.StringVar()
    hist.set("")
    t1 = tk.Label(master=f0.scrollable_frame,textvariable=hist,justify=tk.LEFT)
    tk.Label(master=f1,text="History of dice rolls:",font=fontB,justify=tk.LEFT).grid(row=0,column=2,sticky="nw")
    t1.grid(row=0,column=0,sticky="news")
    tk.Button(master=f1,text="Clear All",font=fontB,bg="pink1",command=lambda:hist.set("")).grid(row=0,column=0,sticky="news",padx=5,pady=5,columnspan=2)
    
    # Create dice buttons
    values = [4,6,8,10,12,20,100]
    labels = ["d4","d6","d8","d10","d12","d20","d100"]
    for i in range(len(labels)):
        makeButton(i,values,labels,f1,hist)     
    e1= tk.Entry(master=f1,width=6)
    e1.grid(row=i+2,column=1,sticky="news")    
    tk.Button(master=f1,text="dX",font=fontB,command=lambda:diceWindow(e1.get(),hist)).grid(row=i+2,column=0,sticky="news")
    f0.grid(row=1,column=2,rowspan=8,sticky="news")    
    f1.grid(row=0,column=0,sticky="news")
    

# Main Window
windows = []
fontSize = 10
fontB = "CourierNew " + str(fontSize) + " bold"
fontF = "CourierNew " + str(fontSize)
root = tk.Tk()
root.title("GORISORs Epic Dice Roller")
root.wm_attributes("-topmost",1)
root.maxsize(220,5000)
root.minsize(220,50)
updateMain(root)

root.mainloop()