from tkinter import *    
import main,Available,showPassword
import client
from tkinter import messagebox

def mainPage():
  root.destroy()
  main.Display()

def deleteService(sId,serviceName,Username):
    check=client.deleteService(sId)
    if(check==0):
        messagebox.showerror(None,"An error has occured")
    elif(check==1):
        messagebox.showinfo(None,"Congrats you deleted a Service!")
        root.destroy()
        Available.Display()
        
def checkService(sId,serviceName,Username):
    check=client.check_service(sId)
    if(check['Password']==None):
        messagebox.showerror(None,"An error has occured")
    elif(check['Password']!=None):
        root.destroy()
        showPassword.Display(sId,serviceName,Username,check['Password'])
        
def Display():
        global root
        root=Tk()
        root.state('zoomed')
        button =Button(text="Main",command=mainPage)
        button.pack(side = BOTTOM)
        test=client.get_services()
        
        #Title
        Label1=Label(root,text="Available Services Page",font=(None,20))
        Label1.place(x=650,y=20)

        #Categories
        Label0=Label(root,text="Check",font=(None,15))
        Label0.place(x=50,y=70)
        Label1=Label(root,text="Delete",font=(None,15))
        Label1.place(x=150,y=70)
        Label2=Label(root,text="Service ID",font=(None,15))
        Label2.place(x=300,y=70)
        Label3=Label(root,text="Service Name",font=(None,15))
        Label3.place(x=500,y=70)
        Label4=Label(root,text="Username",font=(None,15))
        Label4.place(x=700,y=70)
        Label5=Label(root,text="Password",font=(None,15))
        Label5.place(x=1000,y=70)

        yValue=100
        
        for i in range(0,len(test)):
            Button1=Button(root,text="Check",command=lambda i=i:checkService(test[i][0],test[i][1],test[i][2]))
            Button1.place(x=50,y=yValue)
            Button2=Button(root,text="Delete",command=lambda i=i:deleteService(test[i][0],test[i][1],test[i][2]))
            Button2.place(x=150,y=yValue)
            text2=test[i][0]
            myLabel1=Label(root,text=text2)
            myLabel1.place(x=300,y=yValue)
            text2=test[i][1]
            myLabel1=Label(root,text=text2)
            myLabel1.place(x=500,y=yValue)
            text2=test[i][2]
            myLabel1=Label(root,text=text2)
            myLabel1.place(x=700,y=yValue)
            text2=test[i][3]
            myLabel1=Label(root,text=text2)
            myLabel1.place(x=1000,y=yValue)
            yValue+=50
            

        mainloop()
        