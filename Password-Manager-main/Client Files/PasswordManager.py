from tkinter import *
import login,signUp

def loginPage():
    root.destroy()
    login.Display()
    
def signupPage():
    root.destroy()
    signUp.Display()
    
def Display():
    global root
    root=Tk()
    root.state('zoomed')
    root.title("Password Manager page")
    title=Label(root,text="Password Manager",font=(None,40))
    title.pack(pady=20)
    blank=Label(root)
    blank.pack(pady=50)
    #Buttons
    login=Button(root,text="Login!",command=loginPage)
    login.pack()
    signUp=Button(root,text="Sign up!",command=signupPage)
    signUp.pack()
    
    creators=Label(root,text="Created by Artin Biniek,Ethan Leider,Khaled Banjaki,Wei lu",font={None,20})
    creators.pack(pady=100)
    
    
    root.mainloop()
    