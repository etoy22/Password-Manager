from tkinter import *
import tkinter as tk     
import PasswordManager,main
from tkinter import messagebox
import client

def passwordManagerPage():
  root.destroy()
  PasswordManager.Display()

def createAccount():
    print(len(entry_2.get()))
    check=client.setup(entry_1.get(),entry_2.get())
    print(check)
    if(len(entry_2.get())<6):
        messagebox.showerror(None,"Password cant be smaller then 6 letters")
    elif(check==0):
        messagebox.showerror(None,"An error has occured")
    elif(check==1):
        messagebox.showinfo(None,"Congrats you made an Account!")
    elif(check==2):
        messagebox.showerror(None,"There is already an existing user with this Username try to pick a different Username")
    
def Display():
        global root
        global entry_1
        global entry_2
        root=tk.Tk()
        root.state('zoomed')
        label = tk.Label(text="Sign Up page ")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(text="Back",command=passwordManagerPage)
        button.pack(side = BOTTOM)
        label2 = tk.Label(text = "Username ",bg = "white", width = 8, font = ("arial", 10,"bold"))   
        label2.place(x =10, y=130)
        label3 = tk.Label(text = "Password: ",bg = "white", width = 8, font = ("arial", 10,"bold"))   
        label3.place(x =10, y=180)
        submit=tk.Button(text="Submit",command=createAccount)
        submit.place(x=10,y=230)
        entry_1 = tk.Entry(root)
        entry_1.place(x = 80, y =130)
        entry_2 = tk.Entry(root)
        entry_2.place(x = 80, y =180)
        