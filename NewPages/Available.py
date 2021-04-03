from tkinter import *    
import main

def mainPage():
  root.destroy()
  main.Display()
  
def Display():
        global root
        root=Tk()
        #Title
        Label1=Label(root,text="Available Services Page",font=(None,20))
        Label1.place(x=650,y=20)
        #Categories
        Label2=Label(root,text="Services",font=(None,15))
        Label2.place(x=100,y=70)
        Label3=Label(root,text="Username",font=(None,15))
        Label3.place(x=750,y=70)
        Label4=Label(root,text="Password",font=(None,15))
        Label4.place(x=1300,y=70)
        Label14=Label(root,text="View",font=(None,15))
        Label14.place(x=1450,y=70)
        
        #Services Examples
        Label5=Label(root,text="www.google.com",font=(None,10))
        Label5.place(x=100,y=120)
        Label6=Label(root,text="www.clubPenguin.com",font=(None,10))
        Label6.place(x=100,y=170)
        Label7=Label(root,text="www.fakeSite.com",font=(None,10))
        Label7.place(x=100,y=220)
        
        #Username Examples
        Label8=Label(root,text="John Cena!!!",font=(None,10))
        Label8.place(x=750,y=120)
        Label9=Label(root,text="Not Ethan",font=(None,10))
        Label9.place(x=750,y=170)
        Label10=Label(root,text="supercalifragilisticexpialidocious",font=(None,10))
        Label10.place(x=750,y=220)
        
        
        #Password Examples
        Label11=Label(root,text="1234567890",font=(None,10))
        Label11.place(x=1300,y=120)
        Label11.place()
        Label12=Label(root,text="ILoveTacos567",font=(None,10))
        Label12.place(x=1300,y=170)
        Label13=Label(root,text="P$$%^&*iigkb0+",font=(None,10))
        Label13.place(x=1300,y=220)
        
        #View
        Button1=Button(root,text="Show Password")
        Button1.place(x=1430,y=120)
        Button1=Button(root,text="Show Password")
        Button1.place(x=1430,y=170)
        Button1=Button(root,text="Show Password")
        Button1.place(x=1430,y=220)
        

        mainloop()
        