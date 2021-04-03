import GeneratorPage
from tkinter import *
import tkinter as tk

def passwordGeneratorPage():
    #GeneratorPage.Display()
    root.destroy()
    GeneratorPage.Display()
root=tk.Tk()
#generator=Button(root,text="Generator!")  
#passwordGeneratorPage() 
generator=Button(root,text="Generator!",command=passwordGeneratorPage)
generator.pack() 
root.mainloop()   