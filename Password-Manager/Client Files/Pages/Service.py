from tkinter import *
import tkinter as tk     
import main,client
from tkinter import messagebox
def mainPage():
  root.destroy()
  main.Display()

def createService():
    check=client.add_service(entry_3.get(),entry_1.get(),entry_2.get())
    print(check)
    print(client.get_services())
    if(check==0):
        messagebox.showerror(None,"Account is not logged in")
    elif(check==1):
        messagebox.showinfo(None,"Congrats you added a new Service!")
    
def Display():
        global root
        global entry_1
        global entry_2
        global entry_3
        root=tk.Tk()
        root.state('zoomed')
        label = tk.Label(text="Create a New service ")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(text="Main",command=mainPage)
        button.pack(side = BOTTOM)
        label2 = tk.Label(text = "USER  ID: ",bg = "white", width = 8, font = ("arial", 10,"bold"))   
        label2.place(x =10, y=130)
        label3 = tk.Label(text = "Password: ",bg = "white", width = 8, font = ("arial", 10,"bold"))   
        label3.place(x =10, y=180)
        label4 = tk.Label(text = "Service Name: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
        label4.place(x =5, y=230)
        submit=tk.Button(text="Submit",command=createService)
        submit.place(x=10,y=280)
        entry_1 = tk.Entry(root)
        entry_1.place(x = 80, y =130)
        entry_2 = tk.Entry(root)
        entry_2.place(x = 80, y =180)
        entry_3 = tk.Entry(root)
        entry_3.place(x=115, y=230)
        