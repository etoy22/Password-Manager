import sys
import tkinter as tk
from tkinter import filedialog, Text,Scale
import os
import main
sys.path.append('./Helper_Functions')
import Copy
import Generator as gen
def Display():
    global root
    root = tk.Tk()
    root.state('zoomed')
    root.title('Password Generator')
    root.geometry('700x700')
    nums =tk.IntVar(value=1)
    spec = tk.IntVar(value=1)
    ups = tk.IntVar(value=1)
    downs = tk.IntVar(value=1)
    length = tk.IntVar(value=20)

    passed = tk.Entry(root, state='readonly',)
    var = tk.StringVar()
    text = gen.password(20,1,1,1,1)
    var.set(text)
    passed.config(textvariable=var,relief='flat',width = 150, justify='center')
    passed.pack()
    nums =tk.IntVar(value=1)
    spec = tk.IntVar(value=1)
    ups = tk.IntVar(value=1)
    downs = tk.IntVar(value=1)
    length = tk.IntVar(value=20)
    
    def mainPage():
        root.destroy()
        main.Display()
    
    def password():
        '''
        This is a call for a random password
        '''
        global text
        text = gen.password(length.get(),ups.get(),downs.get(),nums.get(),spec.get())
        var.set(text)

    def passwordScale(length):
        '''
        This is a call for a random password for the scale only
        '''
        global text
        text = gen.password(length,ups.get(),downs.get(),nums.get(),spec.get())
        var.set(text)


    def screen():   
        '''
        This is the screen that for the user
        ''' 
        w = Scale(root, from_=1, to=99, orient='horizontal',variable=length, command=passwordScale)
        w.pack()
        c1 = tk.Checkbutton(root, text='Upper Case',onvalue=1, offvalue=0,variable=ups, command=password)
        c1.pack()
        c2 = tk.Checkbutton(root, text='Lower Case',onvalue=1, offvalue=0,variable=downs, command=password)
        c2.pack()
        c3 = tk.Checkbutton(root, text='Number',onvalue=1, offvalue=0,variable=nums, command=password)
        c3.pack()
        c4 = tk.Checkbutton(root, text='Special Character',onvalue=1, offvalue=0,variable=spec, command=password)
        c4.pack()
        copier = tk.Button(root,text = "Copy Password",command=lambda: Copy.copier(text))
        copier.pack()
        main = tk.Button(root,text = "Main",command=mainPage)
        main.pack()
        
    screen()
