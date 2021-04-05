from tkinter import *
import tkinter as tk     
import main

def mainPage():
  root.destroy()
  main.Display()
  
def Display():
        global root
        root=tk.Tk()
        root.state('zoomed')
        label = tk.Label(text="Change Password page ")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(text="Main",command=mainPage)
        button.pack(side = BOTTOM)
        label4 = tk.Label(text = "Change Password: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
        label4.place(x =10, y=130)
        submit=tk.Button(text="Submit")
        submit.place(x=0,y=180)
        entry_3 = tk.Entry()
        entry_3.place(x=140, y=130)
        