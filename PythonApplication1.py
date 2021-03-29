import tkinter as tk              
from tkinter import font as tkfont  
from tkinter import *
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self)
        container.pack(side = "top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight =1)
        container.grid_columnconfigure(0, weight=1)
  

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Password Manager", font=controller.title_font)
        label.pack(side=tk.TOP)

        button1 = tk.Button(self, text="Log  in",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Sign in",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Log in page ", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(side = BOTTOM)
        canvas = tk.Canvas(self, height=500, width=600, bg="white")
        canvas.pack()
        label2 = tk.Label(self,text = "USER  ID: ",bg = "white", width = 8, font = ("arial", 10,"bold"))   
        label2.place(x =10, y=130)
        label3 = tk.Label(self,text = "Password: ",bg = "white", width = 8, font = ("arial", 10,"bold"))   
        label3.place(x =10, y=180)
        entry_1 = tk.Entry(self)
        entry_1.place(x = 80, y =130)
        entry_2 = tk.Entry(self)
        entry_2.place(x = 80, y =180)
 


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Sign in page ", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(side = BOTTOM)
    
        signup_buttom = tk.Button(self, text="Sign up",command=self.sign_up)
        signup_buttom.pack(side = BOTTOM)
        canvas = tk.Canvas(self, height=500, width=600, bg="white")
        canvas.pack()
    
        id_string=tk.StringVar()
        pwd_string=tk.StringVar()
        label2 = tk.Label(self,text = "USER  ID: ",bg = "white", width = 8, font = ("arial", 10,"bold"))   
        label2.place(x =10, y=130)
        label3 = tk.Label(self,text = "Password: ",bg = "white", width = 8, font = ("arial", 10,"bold"))   
        label3.place(x =10, y=180)
        self.entry_1 = tk.Entry(self)
        self.entry_1.place(x = 80, y =130)
        self.id_string = self.entry_1.get()
        self.entry_2 = tk.Entry(self,textvar = pwd_string)
        self.entry_2.place(x = 80, y =180)
        self.pwd_string = self.entry_2.get()
        print(self.pwd_string)
    def sign_up(self):
        a = self.entry_1.get()
        b = self.entry_2.get()
        print("User Id is: "+str(a)+"\n"+ "password is: "+str(b))



if __name__ == "__main__":

    app = SampleApp()
    app.mainloop()
    