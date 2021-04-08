from tkinter import *
import tkinter as tk
from tkinter import messagebox     
import main,PasswordManager
import client

def passwordManagerPage():
    root.destroy()
    PasswordManager.Display()
    
def mainPage():
  check=client.login(entry_1.get(),entry_2.get())
  print(check)
  #Not sure when this ever occurs
  if(check==0):
    messagebox.showerror(None,"An error has occured")
  elif(check==1):
    root.destroy()
    main.Display()
  elif(check==2):
    messagebox.showerror(None,"This account does not exist")
  
  
def Display():
        global root
        global entry_1
        global entry_2
        root=tk.Tk()
        root.state('zoomed')
        label = tk.Label(text="Log in page ")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(text="Back",command=passwordManagerPage)
        button.pack(side = BOTTOM)
        label2 = tk.Label(text = "Username: ",bg = "white", width = 8, font = ("arial", 10,"bold"))   
        label2.place(x =10, y=130)
        label3 = tk.Label(text = "Password: ",bg = "white", width = 8, font = ("arial", 10,"bold"))        
        label3.place(x =10, y=180)
        submit=tk.Button(text="Submit",command=mainPage)
        submit.place(x=10,y=230)
        entry_1 = tk.Entry(root)
        entry_1.place(x = 80, y =130)
        entry_2 = tk.Entry(root)
        entry_2.place(x = 80, y =180)