from tkinter import *    
import main
import client
from tkinter import messagebox
import sentPass
def mainPage():
  root.destroy()
  main.Display()

def deleteSending(recieverUsername,sId):
    print("test")
    check=client.delete_sending(recieverUsername,sId)
    root.destroy()
    sentPass.Display()
    
def sending(recieverUsername,sId):
    check=client.get_send_pass(recieverUsername,sId)
    if(check['Tag']==0):
        messagebox.showerror(None,"Not logged in")
    elif(check['Tag']==1):
        messagebox.showinfo(None,check['Password'][0])
    
        
    
def Display():
        global root
        root=Tk()
        root.state('zoomed')
        button =Button(text="Main",command=mainPage)
        button.pack(side = BOTTOM)
        test=client.sent_password()
        #Title
        Label1=Label(root,text="Outgoing password Page",font=(None,20))
        Label1.place(x=650,y=20)
        #Categories
        Label2=Label(root,text="Service ID",font=(None,15))
        Label2.place(x=100,y=70)
        Label3=Label(root,text="Recievers Username",font=(None,15))
        Label3.place(x=300,y=70)
        Label4=Label(root,text="Service Name",font=(None,15))
        Label4.place(x=600,y=70)
        Label4=Label(root,text="Service Username",font=(None,15))
        Label4.place(x=750,y=70)
        Label4=Label(root,text="Get Password",font=(None,15))
        Label4.place(x=1000,y=70)
        Label4=Label(root,text="Delete",font=(None,15))
        Label4.place(x=1300,y=70)
        entry=list()
        
        yValue=100
        if(test['Info']!=[]):
            
            for i in range(0,len(test['Info'])):
                Button1=Button(root,text="Get",command=lambda i=i:sending(test['Info'][i][2],test['Info'][i][1]))
                Button1.place(x=1000,y=yValue)
                Button2=Button(root,text="Delete",command=lambda i=i:deleteSending(test['Info'][i][2],test['Info'][i][1]))
                Button2.place(x=1300,y=yValue)
                text2=test['Info'][i][1]
                myLabel1=Label(root,text=text2)
                myLabel1.place(x=100,y=yValue)
                text2=test['Info'][i][2]
                myLabel1=Label(root,text=text2)
                myLabel1.place(x=300,y=yValue)
                text2=test['Info'][i][3]
                myLabel1=Label(root,text=text2)
                myLabel1.place(x=600,y=yValue)
                text2=test['Info'][i][4]
                myLabel1=Label(root,text=text2)
                myLabel1.place(x=750,y=yValue)
                
                yValue+=50
        

        mainloop()
        