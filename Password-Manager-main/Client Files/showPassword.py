from tkinter import *
import main,Available

def mainPage():
  root.destroy()
  main.Display()

def AvailablePage():
    root.destroy()
    Available.Display()
    
def Display(sId,serviceName,Username,Password):
        global root
        root=Tk()
        root.state('zoomed')
        button =Button(text="Main",command=mainPage)
        button.pack(side = BOTTOM)
        button =Button(text="Back",command=AvailablePage)
        button.pack(side = BOTTOM)
        Label1=Label(root,text="Display Page",font=(None,20))
        Label1.place(x=650,y=20)
        Label2=Label(root,text="Service ID",font=(None,15))
        Label2.place(x=300,y=70)
        Label3=Label(root,text="Service Name",font=(None,15))
        Label3.place(x=500,y=70)
        Label4=Label(root,text="Username",font=(None,15))
        Label4.place(x=700,y=70)
        Label5=Label(root,text="Password",font=(None,15))
        Label5.place(x=1000,y=70)
        
        myLabel6=Label(root,text=sId)
        myLabel6.place(x=300,y=100)
        
        myLabel7=Label(root,text=serviceName)
        myLabel7.place(x=500,y=100)
        
        myLabel8=Label(root,text=Username)
        myLabel8.place(x=700,y=100)
        
        myLabel9=Label(root,text=Password)
        myLabel9.place(x=1000,y=100)
        root.mainloop()

