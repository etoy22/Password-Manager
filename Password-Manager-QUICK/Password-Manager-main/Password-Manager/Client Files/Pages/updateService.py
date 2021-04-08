from tkinter import *
import tkinter as tk     
import main
from tkinter import messagebox
import client
def mainPage():
  root.destroy()
  main.Display()
        
def changeService():
    print("change service")
    print(client.get_services())
    check=client.update_service(int(entry_1.get()),entry_2.get(),entry_3.get(),entry_4.get())
    print(check['Tag'])
    if(check['Tag']==0):
        messagebox.showerror(None,"Not a valid service ID for this account try choosing a different service ID")
    elif(check['Tag']==1):
        print(client.get_services())
        messagebox.showinfo(None,"Congrats you updated a Service!")
    elif(check['Tag']==2):
        messagebox.showerror(None,"Not a valid service ID for this account try choosing a different service ID")
    
def Display():
        global root
        global entry_1
        global entry_2
        global entry_3
        global entry_4
        root=tk.Tk()
        root.state('zoomed')
        label = tk.Label(text="Change Service page")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(text="Main",command=mainPage)
        button.pack(side = BOTTOM)
        label2 = tk.Label(text = "Service ID: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
        label2.place(x =10, y=130)
        label3 = tk.Label(text = "Service Name: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
        label3.place(x =10, y=180)
        label4 = tk.Label(text = "Username: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
        label4.place(x =10, y=230)
        label5 = tk.Label(text = "Password: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
        label5.place(x =10, y=280)
        update=tk.Button(text="Update",command=changeService)
        update.place(x=10,y=330)
        entry_1 = tk.Entry(root)
        entry_1.place(x =140, y =130)
        entry_2 = tk.Entry(root)
        entry_2.place(x =140, y =180)
        entry_3 = tk.Entry(root)
        entry_3.place(x =140, y =230)
        entry_4 = tk.Entry(root)
        entry_4.place(x =140, y =280)
        
        