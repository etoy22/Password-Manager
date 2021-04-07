from tkinter import *
import tkinter as tk     
import main,client

def mainPage():
  root.destroy()
  main.Display()

def sendingService(sId,value):
    print(sId)
    print(value.get())
   # print(personsUsername)
    
def Display():
        global root
        global entry_1
        root=Tk()
        root.state('zoomed')
        button =Button(text="Main",command=mainPage)
        button.pack(side = BOTTOM)
        print("Send a service:")
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
        for i in range(0,len(test)):
            label2 = tk.Label(text = "Persons Username: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
            label2.place(x =900, y=yValue)
            v=StringVar()
            entry_1 = tk.Entry(root,text=v)
            entry_1.place(x = 1025, y =yValue)
            Button1=Button(root,text="Send",command=lambda:sendingService(test[i][0],v))
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