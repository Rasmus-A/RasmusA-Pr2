from tkinter import *

def add_table(self):
    self.config(cursor='plus')


class MyApplication(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.frames = {}

    def create_frame(self, frame_name, row, column, columnspan):
        frame = MyFrames(self, row, column, columnspan)
        self.frames[frame_name] = frame

class MyFrames(Frame):

    def __init__(self, master, row, column, columnspan):
        Frame.__init__(self, master)
        self.grid(row=row, column=column, columnspan=columnspan)
        self.widgets = {}
        
    def create_label(self, widget_name, text, row, column, columnspan):
            text = StringVar(self, text)
            label = Label(self, textvariable=text)
            self.widgets[widget_name] = label
            label.grid(row=row, column=column, columnspan=columnspan)

    def create_menu_bar(self, widget_name):    #meny är för komplex för att rimligt göra genom en alllmän funltion o måste skapas manuelt, den ligger här för att samla alla widget funktioner
        menubar = Menu(self) #Menybaren

        layoutmenu = Menu(menubar, tearoff=0) #Layout dropdown
        layoutmenu.add_command(label="Add Table", command=lambda: add_table(self))
        layoutmenu.add_command(label="Remove Table", command=)
        layoutmenu.add_separator()
        layoutmenu.add_command(label="Clear Tables", command=)
        menubar.add_cascade(label="Layout", menu=layoutmenu)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save Layout", command=)
        filemenu.add_command(label="Load Layout", command=)
        layoutmenu.add_separator()
        filemenu.add_command(label="Manage Layouts", commands=)
        menubar.add_cascade(label="File", menu=filemenu)



root = Tk()
app = MyApplication(root)
app.create_frame('config_area', 0, 0, 3)

app.create_frame('table_area', 1, 1, 1)

app.create_frame('booking_area', 1, 2, 1)




#app.frames['table_area'].create_widget("hej")
#app.frames['booking_area'].create_widget("då")

root.mainloop()