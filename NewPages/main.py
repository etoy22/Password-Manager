from tkinter import *
from tkinter import messagebox
import GeneratorPage,login,signUp,Username,Password,Service,Sending,Available,Acceptance,PasswordManager
    
def passwordGeneratorPage():
    root.destroy()
    GeneratorPage.Display()
    
def changeUsernamePage():
    root.destroy()
    Username.Display()
    
def changePasswordPage():
    root.destroy()
    Password.Display()
        
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
    root.destroy()
    PasswordManager.Display()

def deleteAccount():
    response=messagebox.askyesno(None,"This will permanently delete your account are you sure you want to continue?")
    if response==1:
        root.destroy()
        PasswordManager.Display()
    else:
        return

def disconnectProgram():
    root.destroy()
       
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
    changeUsername=Button(root,text="Change Username",command=changeUsernamePage)
    changeUsername.pack()
    changePassword=Button(root,text="Change Password",command=changePasswordPage)
    changePassword.pack()
    newService=Button(root,text="New service",command=newServicePage)
    newService.pack()
    availableServices=Button(root,text="Available services",command=availableServicesPage)
    availableServices.pack()
    passwordAcceptance=Button(root,text="Password Acceptance",command=passwordAcceptancePage)
    passwordAcceptance.pack()
    passwordSending=Button(root,text="Password Sending",command=passwordSendingPage)
    passwordSending.pack()
    logOut=Button(root,text="Log Out",command=passwordManagerPage)
    logOut.pack()
    DeleteAccount=Button(root,text="Delete Account",command=deleteAccount)
    DeleteAccount.pack()
    disconnect=Button(root,text="Disconnect",command=disconnectProgram)
    disconnect.pack()
    root.mainloop()
    