
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
        for F in (StartPage, PageTwo):
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
        label = tk.Label(self, text="Server Page", font=controller.title_font)
        label.pack(side=tk.TOP)
        sid_string=tk.StringVar()
        sn_string = tk.StringVar()
        pwd_string=tk.StringVar()
        un_string = tk.StringVar()
        label2 = tk.Label(self,text = "Service  ID: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
        label2.place(x =10, y=130)
        label3 = tk.Label(self,text = "Service name: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
        label3.place(x =10, y=180)
        label4 = tk.Label(self,text = "User name: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
        label4.place(x =10, y=230)
        label5 = tk.Label(self,text = "password: ",bg = "white", width = 15, font = ("arial", 10,"bold"))   
        label5.place(x =10, y=280)
        submit_buttom = tk.Button(self, text="Submit",command=lambda: controller.show_frame("PageTwo"))
        submit_buttom.pack(side = BOTTOM)
        self.entry_1 = tk.Entry(self)
        self.entry_1.place(x = 150, y =130)
        self.id_string = self.entry_1.get()
        self.entry_2 = tk.Entry(self,textvar = pwd_string)
        self.entry_2.place(x = 150, y =180)
        self.pwd_string = self.entry_2.get()
        self.entry_3 = tk.Entry(self)
        self.entry_3.place(x =150, y =230)
        self.entry_4 = tk.Entry(self)
        self.entry_4.place(x =150, y =280)
       
    def Submit(self):
        a = self.entry_1.get()
        b = self.entry_2.get()
        print("User Id is: "+str(a)+"\n"+ "password is: "+str(b))



class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = tk.Canvas(self, height=500, width=600, bg="white")
        canvas.pack()
        clicked = tk.StringVar()
        clicked.set("show all the servers")
        var = tk.StringVar()
        var.set("serves id 7, servers name ab, use name abc, password nb!")
        def print_se(self):
            print(var.get())
        lst = ["a","b","c","d","e","f"]
        lst.append(var.get())
        drop = OptionMenu(self, clicked, *lst)
        drop.place(x =150, y =230)

    def sign_up(self):
        a = self.entry_1.get()
        b = self.entry_2.get()
        print("User Id is: "+str(a)+"\n"+ "password is: "+str(b))



if __name__ == "__main__":

    app = SampleApp()
    app.mainloop()
    