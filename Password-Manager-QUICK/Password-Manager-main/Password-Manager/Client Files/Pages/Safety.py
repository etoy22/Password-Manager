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
        test=client.ver()
        print(client.ver())
        #Title
        Label1=Label(root,text="Safety check Page",font=(None,20))
        Label1.place(x=650,y=20)
        #Categories
        Label2=Label(root,text="Service ID",font=(None,15))
        Label2.place(x=100,y=70)
        Label3=Label(root,text="Service Name",font=(None,15))
        Label3.place(x=300,y=70)
        Label4=Label(root,text="Username",font=(None,15))
        Label4.place(x=600,y=70)
        Label4=Label(root,text="Smaller then 6",font=(None,15))
        Label4.place(x=900,y=70)
        Label4=Label(root,text="Repeated",font=(None,15))
        Label4.place(x=1200,y=70)
        entry=list()
        print()
        yValue=100
        #To print first one completely
        
        for i in range(len(test['Info'])):
            temp="No"
            text2=test['Info'][i][0]
            myLabel1=Label(root,text=text2)
            myLabel1.place(x=100,y=yValue)
            text2=test['Info'][i][1]
            myLabel1=Label(root,text=text2)
            myLabel1.place(x=300,y=yValue)
            text2=test['Info'][i][2]
            myLabel1=Label(root,text=text2)
            myLabel1.place(x=600,y=yValue)
            if(test['Info'][i][4]==1):
                text2="Yes"
            elif(test['Info'][i][4]==0):
                text2="No"
            myLabel1=Label(root,text=text2)
            myLabel1.place(x=900,y=yValue)
            if(test['Info'][i][5]==1):
                text2="Yes"
            elif(test['Info'][i][5]==0):
                text2="No"
            myLabel1=Label(root,text=text2)
            myLabel1.place(x=1200,y=yValue)
            yValue+=50

        mainloop()
        