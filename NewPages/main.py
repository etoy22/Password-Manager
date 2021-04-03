from tkinter import *
import GeneratorPage,login,signUp,Username,Password,Service,Sending,Available,Acceptance
#import os
#root=Tk()
def loginPage():
    root.destroy()
    login.Display()
    
def signupPage():
    root.destroy()
    signUp.Display()
    
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
    
def Display():
    global root
    root=Tk()
    root.title("Main page")
    title=Label(root,text="Password Manager :D",font=(None,40))
    title.pack(pady=20)
    #Buttons
    login=Button(root,text="Login!",command=loginPage)
    login.pack()
    signUp=Button(root,text="Sign up!",command=signupPage)
    signUp.pack()
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
    
    creators=Label(root,text="Created by Artin the best,Ethan the man,Kbaan the swagger,Wei the master",font={None,20})
    creators.pack(pady=200)
    
    
    root.mainloop()
    