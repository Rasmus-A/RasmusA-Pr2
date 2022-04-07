from tkinter import *
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Prog2'
)
myursor = mydb.cursor()
    


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
        layoutmenu.add_command(label="Add Table", command=add_table)
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

        def add_table():
            def table_menu(event):
                def create_2(event):
                    sql = "INSERT INTO Tables (ID, Size, CenterX, CenterY) VALUES (%s, %s, %s, %s)"
                    val = 
                def create_4(event):
                    pass
                popup = Menu(self, tearoff=0)
                popup.add_command(label="Cluster of 2", command=create_2)
                popup.add_command(label="Cluster of 4", command=create_4)
                popup.add_separator()
                popup.add_command(label="Cancel", command=lambda: break)

                try:    #Behövs den?
                    popup.tk_popup(event.x, event.y, 0)
                finally:
                    popup.grab_realease()

            self.config(cursor='plus')
            self.bind('<Button-1>', table_menu)

root = Tk()
app = MyApplication(root)
app.create_frame('config_area', 0, 0, 3)

app.create_frame('table_area', 1, 1, 1)

app.create_frame('booking_area', 1, 2, 1)




#app.frames['table_area'].create_widget("hej")
#app.frames['booking_area'].create_widget("då")

root.mainloop()