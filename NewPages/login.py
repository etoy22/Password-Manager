from tkinter import *
import tkinter as tk     
import main,PasswordManager

def passwordManagerPage():
    root.destroy()
    PasswordManager.Display()
    
def mainPage():
  root.destroy()
  main.Display()
  
def Display():
        global root
        root=tk.Tk()
        root.state('zoomed')
        label = tk.Label(text="Log in page ")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(text="Back",command=passwordManagerPage)
        button.pack(side = BOTTOM)
        label2 = tk.Label(text = "USER  ID: ",bg = "white", width = 8, font = ("arial", 10,"bold"))   
        label2.place(x =10, y=130)
        label3 = tk.Label(text = "Password: ",bg = "white", width = 8, font = ("arial", 10,"bold"))        
        label3.place(x =10, y=180)
        submit=tk.Button(text="Submit",command=mainPage)
        submit.place(x=10,y=230)
        entry_1 = tk.Entry()
        entry_1.place(x = 80, y =130)
        entry_2 = tk.Entry()
        entry_2.place(x = 80, y =180)