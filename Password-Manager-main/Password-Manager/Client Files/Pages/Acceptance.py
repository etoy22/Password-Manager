from tkinter import *    
import main
import client

def mainPage():
  root.destroy()
  main.Display()

def confirm(sId,value):
    print(sId)
    print(value.get())
    
def Display():
        global root
        root=Tk()
        root.state('zoomed')
        button =Button(text="Main",command=mainPage)
        button.pack(side = BOTTOM)
        test=client.get_services()
        #Title
        Label1=Label(root,text="Acceptance Page",font=(None,20))
        Label1.place(x=650,y=20)
        #Categories
        Label2=Label(root,text="Service ID",font=(None,15))
        Label2.place(x=100,y=70)
        Label3=Label(root,text="Service Name",font=(None,15))
        Label3.place(x=300,y=70)
        Label4=Label(root,text="Username",font=(None,15))
        Label4.place(x=600,y=70)
        Label4=Label(root,text="Accept Service",font=(None,15))
        Label4.place(x=900,y=70)
        Label4=Label(root,text="Send",font=(None,15))
        Label4.place(x=1200,y=70)
        Label4=Label(root,text="Delete",font=(None,15))
        Label4.place(x=1300,y=70)
        entry=list()
        yValue=100
        
        for i in range(0,len(test)):
            label2 =Label(text = "Password: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
            label2.place(x =900, y=yValue)
            entry.append(Entry())
            entry[i].place(x = 1025, y =yValue)
            Button1=Button(root,text="Send",command=lambda i=i:confirm(test[i][0],entry[i]))
            Button1.place(x=1200,y=yValue)
            Button2=Button(root,text="Delete",command=lambda i=i:confirm(test[i][0],entry[i]))
            Button2.place(x=1300,y=yValue)
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
        

        mainloop()
        