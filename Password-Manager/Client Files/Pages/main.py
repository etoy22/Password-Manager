from tkinter import *
from tkinter import messagebox
import GeneratorPage,login,signUp,Service,updateService,Sending,Available,Acceptance,PasswordManager,client
    
def passwordGeneratorPage():
    root.destroy()
    GeneratorPage.Display()
    
def updateServicePage():
    root.destroy()
    updateService.Display()
        
def newServicePage():
    root.destroy()
    Service.Display()
    
def availableServicesPage():
     root.destroy()
     Available.Display()
    
def passwordAcceptancePage():
    root.destroy()
    Acceptance.Display()  
    
def passwordSendingPage():
    root.destroy()
    Sending.Display() 

def passwordManagerPage():
    check=client.logout()
    print(check)
    if (check==0):
         messagebox.showerror(None,"An error has occured")
    elif(check==1):
        root.destroy()
        PasswordManager.Display()

def deleteAccount():
    response=messagebox.askyesno(None,"This will permanently delete your account are you sure you want to continue?")
    if response==1:
        check=client.delete_account()
        print(check)
        if(check==0):
            messagebox.showerror(None,"An error has occured")
        elif(check==1):
            root.destroy()
            PasswordManager.Display()
    else:
        return
       
def Display():
    global root
    root=Tk()
    root.state('zoomed')
    root.title("Main page")
    title=Label(root,text="Main Page",font=(None,20))
    title.pack(pady=20)
    #Buttons
    generator=Button(root,text="Generator!",command=passwordGeneratorPage)
    generator.pack()
    newService=Button(root,text="New service",command=newServicePage)
    newService.pack()
    updateService=Button(root,text="Update Service",command=updateServicePage)
    updateService.pack()
    availableServices=Button(root,text="Available services",command=availableServicesPage)
    availableServices.pack()
    passwordAcceptance=Button(root,text="Password Acceptance",command=passwordAcceptancePage)
    passwordAcceptance.pack()
    passwordSending=Button(root,text="Password Sending",command=passwordSendingPage)
    passwordSending.pack()
    DeleteAccount=Button(root,text="Delete Account",command=deleteAccount)
    DeleteAccount.pack()
    logOut=Button(root,text="Log Out",command=passwordManagerPage)
    logOut.pack()
    root.mainloop()
    