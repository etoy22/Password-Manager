from tkinter import *
import tkinter as tk     
import main

def mainPage():
  root.destroy()
  main.Display()
def Display():
        global root
        root=tk.Tk()
        label = tk.Label(text="Send a Password ")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(text="Main",command=mainPage)
        button.pack(side = BOTTOM)
        label2 = tk.Label(text = "Your USER  ID: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
        label2.place(x =10, y=130)
        label3 = tk.Label(text = "Your Password: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
        label3.place(x =10, y=180)
        label4 = tk.Label(text = "Persons User ID: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
        label4.place(x =10, y=230)
        submit=tk.Button(text="Submit")
        submit.place(x=10,y=280)
        entry_1 = tk.Entry()
        entry_1.place(x = 120, y =130)
        entry_2 = tk.Entry()
        entry_2.place(x = 120, y =180)
        entry_3 = tk.Entry()
        entry_3.place(x=125, y=230)
        