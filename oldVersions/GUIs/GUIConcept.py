"""
    Version 1 of the program
    Date: early June 2023
    The purpose of this program is to get a visual Representation of what the GUI for this project should look like

"""


import tkinter as tk
import os
import sqlite3 
from tkinter import *
#from PIL import ImageTk,IMAGE
from tkinter import ttk
root = tk.Tk()
#              Xaxis, Yaxis
root.geometry('1000x600')
root.title('GUI Concept')

import random
import numpy as np
state = '' 
#canvas = tk.Canvas(root, height=200, width=600 )
#Canvas()
#tk.Canvas(root, height=1000, width=600, )

posInt=5

def login_page():
    global posInt

    def forwardSelf():
        global posInt
        #register_page()
        global state
        state = 'Login'
        posInt=posInt+5
        currentFrame.destroy()
        #canvas.delete(circleShape)
        #canvas.delete(centerForce)

        #canvas.destroy()
        mainMenu()


    def forward_register_page():
        #register_page()
        global state
        state = 'Register'
        currentFrame.destroy()
        mainMenu()

    def forward_dashboard():
        global state
        state = 'Dashboard'
        currentFrame.destroy()
        mainMenu()

    def forward_admin_dashboard():
        global state
        state = 'AdminDashboard'
        currentFrame.destroy()
        mainMenu()

    def verify():
        print("yes")

    currentFrame = tk.Frame(root, relief=tk.RIDGE)
   
    canvas = tk.Canvas(currentFrame, width =1000, height=600 )


    nextButton = tk.Button(currentFrame, text='Next Datapoint', font=('Bold',12),
                            bg= '#158aff', fg='white', command=verify)
    nextButton.place(x=800, y=100, width=150)  

    previousButton = tk.Button(currentFrame, text='Previous Datapoint', font=('Bold',12),
                            bg= '#158aff', fg='white', command=verify)
    previousButton.place(x=600, y=100, width=150) 

    resizeButton = tk.Button(currentFrame, text='Manual', font=('Bold',12),
                            bg= '#158aff', fg='white', command=forwardSelf)
    resizeButton.place(x=600 , y=200, width=150)   
    
    var=10
    #{currentFrame.getname()}
    name_lb = tk.Label(currentFrame, text= f"Cog at time: {var}", font=('Bold',12))
    name_lb.place(x=600,y=50)
    

    thumbPos=[50,300]
    thumbMarker=canvas.create_oval(thumbPos[0]-10,thumbPos[1]-10,thumbPos[0]+10, thumbPos[1]+10, outline = "black", fill = "purple",width = 2)
    thumbText=canvas.create_text(thumbPos[0], thumbPos[1]-40, text="Sensor1, Thumb", fill="black", font=('Helvetica 8 bold'))
    thumbText=canvas.create_text(thumbPos[0], thumbPos[1]-20, text="40 kPa", fill="black", font=('Helvetica 8 bold'))

    middlePos=[400,100]
    middleMarker=canvas.create_oval(middlePos[0]-10,middlePos[1]-10,middlePos[0]+10, middlePos[1]+10, outline = "black", fill = "blue",width = 2)
    middleText=canvas.create_text(middlePos[0], middlePos[1]-40, text="Middle Finger", fill="black", font=('Helvetica 8 bold'))
    middleForceText=canvas.create_text(middlePos[0], middlePos[1]-20, text="50 kPa", fill="black", font=('Helvetica 8 bold'))

    pointerPos=[400,500]
    pointerMarker=canvas.create_oval(pointerPos[0]-10,pointerPos[1]-10,pointerPos[0]+10, pointerPos[1]+10, outline = "black", fill = "blue",width = 2)
    pointerText=canvas.create_text(pointerPos[0], pointerPos[1]-40, text="Pointer finger", fill="black", font=('Helvetica 8 bold'))
    pointerForceText=canvas.create_text(pointerPos[0], pointerPos[1]-20, text="22 kPa", fill="black", font=('Helvetica 8 bold'))
    
    centerPos=[200,300]
    circleShape=canvas.create_oval((centerPos[0]-10 + posInt), centerPos[1]-10, (centerPos[0]+10 + posInt), centerPos[1]+10, outline = "black", fill = "red",width = 2)
    centerText=canvas.create_text(centerPos[0] + posInt, centerPos[1]-40, text="Center of Force", fill="black", font=('Helvetica 8 bold'))
    centerForceText=canvas.create_text(centerPos[0] + posInt, centerPos[1]-20, text="no force?", fill="black", font=('Helvetica 8 bold'))


    canvas.pack()

    currentFrame.pack(pady=10)
    currentFrame.pack_propagate(False)

    #login_frame.configure(height=400, width=250, bg='gray')
    currentFrame.configure(height=600, width=1000)





def register_page():
    def forward_login_page():
        register_frame.destroy()
        #login_page()
        global state
        state = 'Login'

        mainMenu()
    def verify():
        print("yes")
    ###        
    register_frame =tk.Frame(root)

    #enter email
    email_lb = tk.Label(register_frame, text='Enter Email', font=('Bold',12))
    email_lb.place(x=160,y=20)

    email = tk.Entry(register_frame, font=('Bold', 15), bd=0, highlightcolor='#158aff',
                        highlightthickness=2, highlightbackground='gray')
    email.place(x=150, y=60, width=250, height=30)
    #enter name
    username_lb = tk.Label(register_frame, text='Enter Username', font=('Bold',12))
    username_lb.place(x=160,y=100)

    username = tk.Entry(register_frame, font=('Bold', 15), bd=0, highlightcolor='#158aff',
                        highlightthickness=2, highlightbackground='gray')
    username.place(x=150, y=140, width=250, height=30)
    #enter address
    address_lb = tk.Label(register_frame, text='Enter Address', font=('Bold',12))
    address_lb.place(x=160,y=180)

    address = tk.Entry(register_frame, font=('Bold', 15), bd=0, highlightcolor='#158aff',
                        highlightthickness=2, highlightbackground='gray')
    address.place(x=150, y=220, width=250, height=30)
    #enter phone number
    pnumber_lb = tk.Label(register_frame, text='Enter Phone Number', font=('Bold',12))
    pnumber_lb.place(x=160,y=260)

    pnumber = tk.Entry(register_frame, font=('Bold', 15), bd=0, highlightcolor='#158aff',
                        highlightthickness=2, highlightbackground='gray')
    pnumber.place(x=150, y=300, width=250, height=30)
    #enter password
    password_lb =tk.Label(register_frame, text='Enter Password', font=('Bold',12))
    password_lb.place(x=160, y=340) 

    password = tk.Entry(register_frame, font=('Bold',15), bd=0, highlightcolor='#158aff',
                        highlightthickness=2, highlightbackground='gray')
    password.place(x=150, y=380, width=250, height=30)     
    #repeat password
    repeat_password_lb =tk.Label(register_frame, text='Repeat Password', font=('Bold',12))
    repeat_password_lb.place(x=160, y=420) 

    repeat_password = tk.Entry(register_frame, font=('Bold',15), bd=0, highlightcolor='#158aff',
                        highlightthickness=2, highlightbackground='gray')
    repeat_password.place(x=150, y=460, width=250, height=30)     

    register_btn = tk.Button(register_frame, text='Register', font=('Bold',12),
                            bg= '#158aff', fg='white',command =verify)
    register_btn.place(x=150, y=500, width=150)

    login_page_link = tk.Button(register_frame, text= 'Login', fg='#158aff',underline=True,
                                font=('Bold', 12), bd=0, command=forward_login_page)

    login_page_link.place(x=200, y=540 )                            

    register_frame.pack()
    register_frame.pack_propagate(False)
    register_frame.configure(height= 600, width = 1000)



state = 'Login'

login_page()

#state block

def mainMenu():
    if state == 'Login':
        login_page()
    elif state == "Register":
        register_page() 
    else:
        print("Goodbye")
mainMenu()

root.mainloop()