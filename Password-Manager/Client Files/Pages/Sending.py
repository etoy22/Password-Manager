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
        label = tk.Label(text="Send a Password ")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(text="Main",command=mainPage)
        button.pack(side = BOTTOM)
        label2 = tk.Label(text = "Persons USER ID: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
        label2.place(x =10, y=130)
        submit=tk.Button(text="Submit")
        submit.place(x=10,y=180)
        entry_1 = tk.Entry()
        entry_1.place(x = 140, y =130)
        