from tkinter import *    
import main

def mainPage():
  root.destroy()
  main.Display()
  
def Display():
        global root
        root=Tk()
        root.state('zoomed')
        button =Button(text="Main",command=mainPage)
        button.pack(side = BOTTOM)
        #Title
        Label1=Label(root,text="Acceptance Page",font=(None,20))
        Label1.place(x=650,y=20)
        #Categories
        Label2=Label(root,text="User Id's",font=(None,15))
        Label2.place(x=100,y=70)
        Label3=Label(root,text="Password",font=(None,15))
        Label3.place(x=750,y=70)
        Label4=Label(root,text="Accept",font=(None,15))
        Label4.place(x=1300,y=70)
        
        #User Id Examples
        Label5=Label(root,text="Chuck norris",font=(None,10))
        Label5.place(x=100,y=120)
        Label6=Label(root,text="Steve job",font=(None,10))
        Label6.place(x=100,y=170)
        Label7=Label(root,text="cryptoIsCool",font=(None,10))
        Label7.place(x=100,y=220)
        
        #Password Examples
        Label8=Label(root,text="98hdjsl",font=(None,10))
        Label8.place(x=750,y=120)
        Label9=Label(root,text="lmnoskaqidngdkskdk0099",font=(None,10))
        Label9.place(x=750,y=170)
        Label10=Label(root,text="iopi#ak$fmosoj$$%%11-0",font=(None,10))
        Label10.place(x=750,y=220)
        
        #Accept
        entry1 =Entry()
        entry1.place(x = 1300, y =120)
        entry2 =Entry()
        entry2.place(x = 1300, y =170)
        entry3 =Entry()
        entry3.place(x = 1300, y =220)
        
        #View
        Button1=Button(root,text="Submit")
        Button1.place(x=1430,y=120)
        Button2=Button(root,text="Submit")
        Button2.place(x=1430,y=170)
        Button3=Button(root,text="Submit")
        Button3.place(x=1430,y=220)
        

        mainloop()
        