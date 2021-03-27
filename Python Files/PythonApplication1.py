import tkinter as tk
from tkinter import filedialog, Text
import os
root = tk.Tk()
canvas = tk.Canvas(root, height=700, width=700, bg="black")
canvas.pack()

frame = tk.Frame(root,bg ="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
def log_Window():
    newWindow = tk.Toplevel(frame)
    newWindow.title("log in page")
    newWindow.geometry("400x400")
def sign_Window():
    newWindow = tk.Toplevel(frame)
    newWindow.title("sign in page")
    newWindow.geometry("400x400")

    


log_in = tk.Button(frame,text = "Log in", fg="white", bg="black", command = log_Window)
log_in.pack(padx =10, pady=5, side= tk.BOTTOM)

sign_in = tk.Button(frame,text = "sign in", fg="white", bg="black",command = sign_Window)
sign_in.pack(padx =10, pady=5, side= tk.BOTTOM)

root.mainloop()