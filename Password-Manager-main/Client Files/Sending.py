from tkinter import *
import tkinter as tk     
import main,client
from tkinter import messagebox
def mainPage():
  root.destroy()
  main.Display()
        
def sendingService(sId,value):
        temp=value.get()
        check=client.send_account(temp,sId)
        print(check)
        if(check['Tag']==0):
             messagebox.showerror(None,"Account is not logged in")
        elif(check['Tag']==1):
            messagebox.showinfo(None,"This is the password your going to have to give! Password: "+check['Password'])
        elif(check['Tag']==2):
            messagebox.showinfo(None,"You have resent this service!")
        elif(check['Tag']==3):
            messagebox.showinfo(None,"Congrats you sent this service to yourself!")
        elif(check['Tag']==4):
            messagebox.showerror(None,"User does not exist")

def Display():
        global root
        root=Tk()
        root.state('zoomed')
        button =Button(text="Main",command=mainPage)
        button.pack(side = BOTTOM)
        test=client.get_services()
        
        #Title
        Label1=Label(root,text="Sending Services Page",font=(None,20))
        Label1.place(x=650,y=20)

        #Categories
        Label2=Label(root,text="Service ID",font=(None,15))
        Label2.place(x=100,y=70)
        Label3=Label(root,text="Service Name",font=(None,15))
        Label3.place(x=300,y=70)
        Label4=Label(root,text="Username",font=(None,15))
        Label4.place(x=600,y=70)
        Label4=Label(root,text="Persons Username",font=(None,15))
        Label4.place(x=900,y=70)
        Label4=Label(root,text="Send",font=(None,15))
        Label4.place(x=1200,y=70)    

        yValue=100
        entry=list()
        for i in range(0,len(test)):
            entry.append(Entry())
            entry[i].place(x = 900, y =yValue)
            Button1=Button(root,text="Send",command=lambda i=i:sendingService(test[i][0],entry[i]))
            Button1.place(x=1200,y=yValue)
            text2=test[i][0]
            myLabel1=Label(root,text=text2)
            myLabel1.place(x=100,y=yValue)
            text2=test[i][1]
            myLabel1=Label(root,text=text2)
            myLabel1.place(x=300,y=yValue)
            text2=test[i][2]
            myLabel1=Label(root,text=text2)
            myLabel1.place(x=600,y=yValue)
            yValue+=50
            
        root.mainloop()