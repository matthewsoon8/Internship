"""
    Version 2 of the program
    Date:   early June 2023
    Purpose:The purpose of this program is to get a visual Representation of what the GUI for this project should look like
    Notes:  This program reads the Results.xlsx file and allows the user to click through each Data point and see where
    the COP is at any point in time
"""

import tkinter as tk
import os
import sqlite3
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import numpy as np

import pandas as pd
import statistics
from matplotlib import pyplot as plt

filePath='results.xlsx'

#df= pd.read_excel(filePath,sheet_name=[1])

df = pd.read_excel(filePath, sheet_name=2)


array_data = df.values

list_data = df.values.tolist()

temp=''
increaseIndex=3
indexArr=[]
pinkyArr=[]
thumbArr=[]
iterationIndex=1

while pd.isnull(temp) ==False:
    temp = list_data[increaseIndex][1]
    temp2= list_data[increaseIndex][2]
    temp3 = list_data[increaseIndex][3]
    #print(temp)
    indexArr.append(temp )
    pinkyArr.append(temp2)
    thumbArr.append(temp3)
    increaseIndex=increaseIndex+1

iteration1 =[]
iteration1.append(indexArr)
iteration1.append(pinkyArr)
iteration1.append(thumbArr)
print( len(iteration1[1]) )

print(iteration1)

######################################################################################


root = tk.Tk()
fig, ax = plt.subplots()
root.geometry('1000x1000')
root.title('GUI 2')
state = ''

pointIndex=0

def graphPage():
    global state
    global pointIndex
    def forwardSelf():
        print(pointIndex)
        ax.clear()  # Clear previous points
        state = 'Login'
        fig.canvas.draw()
        fig.canvas.flush_events()
        currentFrame.destroy()
        mainMenu()

    def increaseIndex(increaseNum):
        global pointIndex
        if( pointIndex< len(iteration1[1])-increaseNum ):
            pointIndex=pointIndex+increaseNum
        forwardSelf()
    def decreaseIndex(decreaseNum):
        global pointIndex
        if(pointIndex> 0+decreaseNum):
            pointIndex=pointIndex-decreaseNum
        forwardSelf()

    
    def on_closing():
        root.destroy()  # Close the window and stop the event loop



    currentFrame = tk.Frame(root, relief=tk.RIDGE)
    currentFrame.pack(side=RIGHT)
    currentFrame.pack_propagate(False)

    currentFrame.configure(height=600, width=1000)

    canvas = FigureCanvasTkAgg(fig, master=currentFrame)
    canvas.get_tk_widget().pack(side=LEFT)

    pinkyCoord=[10, 1]
    ax.plot(pinkyCoord[0], pinkyCoord[1],'-ro')
    ax.text(10-0.5, 1 +0.5,"Pinky")

    indexCoord= [pinkyCoord[0], pinkyCoord[1]+10]
    ax.plot(indexCoord[0], indexCoord[1],'-bo')
    ax.text(10-0.5, 11 +0.5,"Index")
    
    thumbCoord= [pinkyCoord[0]-8.485, pinkyCoord[1]+7]
    ax.plot(thumbCoord[0], thumbCoord[1],'-go')
    ax.text(10-8.485 -0.5, 8 +0.5,"Thumb")

    force=[ float(iteration1[0][pointIndex]),float(iteration1[1][pointIndex]),float(iteration1[2][pointIndex]) ]

    if( (force[0]+force[1]+force[2])==0):
        xPoint=0;
        yPoint=0;
    else:
        xPoint=( pinkyCoord[0]*force[0] + indexCoord[0]*force[1] + thumbCoord[0]*force[2] ) /(force[0]+force[1]+force[2])
        yPoint=( pinkyCoord[1]*force[0]  +indexCoord[1]*force[1] + thumbCoord[1] *force[2]  )/(force[0]+force[1]+force[2])

    ax.plot(xPoint, yPoint,'-go')
    ax.text(xPoint -0.5, yPoint +0.5,"Center of Gravity")

    skipForwardButton = tk.Button(currentFrame, text='Skip forward 10', font=('Bold', 12),
                           bg='#158aff', fg='white',command=lambda number=10: increaseIndex(number))
    skipForwardButton.place(x=820, y=50, width=150)
    
    nextButton = tk.Button(currentFrame, text='Next Datapoint', font=('Bold', 12),
                           bg='#158aff', fg='white',command=lambda number=1: increaseIndex(number) )
    nextButton.place(x=820, y=100, width=150)

    skipBackwardButton = tk.Button(currentFrame, text='Skip Backward 10', font=('Bold', 12),
                           bg='#158aff', fg='white',command=lambda number=10: decreaseIndex(number))
    skipBackwardButton.place(x=650, y=50, width=150)

    previousButton = tk.Button(currentFrame, text='Previous Datapoint', font=('Bold', 12),
                               bg='#158aff', fg='white', command=lambda number=1: decreaseIndex(number) )
    previousButton.place(x=650, y=100, width=150)

    """
    resizeButton = tk.Button(currentFrame, text='Manual', font=('Bold', 12),
                             bg='#158aff', fg='white', command=forwardSelf)
    resizeButton.place(x=600, y=200, width=150)
    """
    rating_label = tk.Label(currentFrame, text= f"Time in seconds: {pointIndex}", font=('Bold',12))
    rating_label.place(x=800,y=300)

    rating_label = tk.Label(currentFrame, text= f"Iteration #{iterationIndex}", font=('Bold',12))
    rating_label.place(x=800,y=200)

state = 'graphPage'

def mainMenu():
    if state == 'graphPage':
        graphPage()
    elif state == "Register":
        print("state 2")
    else:
        print("Goodbye")

mainMenu()
root.mainloop()
