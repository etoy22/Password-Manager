from tkinter import *    
import main
import client
from tkinter import messagebox
import Acceptance
def mainPage():
  root.destroy()
  main.Display()

def deleteREC(sendersUsername,sId):
    print("delete")
    print(sendersUsername)
    print(sId)
    check=client.delete_rec(sendersUsername,sId)
    print("check:")
    print(check)
    
def sending(senderUsername,sId,value):
    print(sId)
    print(senderUsername)
    temp=value.get()
    check=client.rec_acc_pass(senderUsername,sId,temp)
    if(check['Tag']==0):
        messagebox.showerror(None,"An error has occured")
    elif(check['Tag']==1):
        messagebox.showinfo(None,"Congrats its been transferred!")
        root.destroy()
        Acceptance.Display()
    elif(check['Tag']==2):
        messagebox.showerror(None,"Entered wrong password")
    
        
    
def Display():
        global root
        root=Tk()
        root.state('zoomed')
        button =Button(text="Main",command=mainPage)
        button.pack(side = BOTTOM)
        test=client.rec_acc()
        print(test)
        #Title
        Label1=Label(root,text="Acceptance Page",font=(None,20))
        Label1.place(x=650,y=20)
        #Categories
        Label2=Label(root,text="Service ID",font=(None,15))
        Label2.place(x=100,y=70)
        Label3=Label(root,text="Senders Username",font=(None,15))
        Label3.place(x=300,y=70)
        Label4=Label(root,text="Service Name",font=(None,15))
        Label4.place(x=600,y=70)
        Label4=Label(root,text="Service Username",font=(None,15))
        Label4.place(x=750,y=70)
        Label4=Label(root,text="Accept Service",font=(None,15))
        Label4.place(x=950,y=70)
        Label4=Label(root,text="Send",font=(None,15))
        Label4.place(x=1200,y=70)
        Label4=Label(root,text="Delete",font=(None,15))
        Label4.place(x=1300,y=70)
        entry=list()
        yValue=100
        print(test['Info'])
        if(test['Info']!=[]):
            
            for i in range(0,len(test['Info'])):
                label2 =Label(text = "Password: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
                label2.place(x =950, y=yValue)
                entry.append(Entry())
                entry[i].place(x = 1075, y =yValue)
                Button1=Button(root,text="Send",command=lambda i=i:sending(test['Info'][i][2],test['Info'][i][1],entry[i]))
                Button1.place(x=1200,y=yValue)
                Button2=Button(root,text="Delete",command=lambda i=i:deleteREC(test['Info'][i][2],test['Info'][i][1]))
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
        