from tkinter import *
from turtle import bgcolor
import mysql.connector
from mysqlx import Column

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Prog2'
)
myursor = mydb.cursor()

def donothing():
    pass

root = Tk()

#skapar frames
config_area = Frame(root, bg='red')
table_area = Frame(root, bg='green')
bookings_area = Frame(root, bg='blue')

#main frame layout
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

config_area.grid(column=0, sticky=W)
table_area.grid(column=1, sticky=NS)
bookings_area.grid(column=2, sticky=E)

#skapar config_area widgets
label = Label(config_area, text="kuk")


#config_area layout
label.grid(row=1,column=1)


def add_table():
    def table_popup(event):
        popup = Menu(table_area, tearoff=0)
        popup.add_command(label="Cluster of 2", command=donothing)
        popup.add_command(label="Cluster of 4", command=donothing)
        popup.add_separator()
        popup.add_command(label="Cancel", command=lambda: add_table)

        try:
            popup.tk_popup(event.x, event.y, 0)
        except: popup.grab_release()

    table_area.config(cursor='plus')
    table_area.bind('<Button-1>', table_popup)
    pass

def remove_table(): #Radera ett bord
    pass

def clear_tables(): #Radera alla bord
    pass

def save_layout():
    pass

def load_layout():
    pass

def manage_layouts():
    pass

"""
menubar = Menu(table_area) #Menybaren
layoutmenu = Menu(menubar, tearoff=0) #Layout dropdown
layoutmenu.add_command(label="Add Table", command=add_table)
layoutmenu.add_command(label="Remove Table", command=remove_table)
layoutmenu.add_separator()
layoutmenu.add_command(label="Clear Tables", command=clear_tables)
menubar.add_cascade(label="Layout", menu=layoutmenu)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Save Layout", command=save_layout)
filemenu.add_command(label="Load Layout", command=load_layout)
filemenu.add_separator()
filemenu.add_command(label="Manage Layouts", command=manage_layouts)
#menubar.add_cascade(label="File", menu=filemenu)
"""
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Save layout", command=donothing)
filemenu.add_command(label="Load layout", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Manage layouts", command=donothing)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Add table", command=donothing)
editmenu.add_command(label="Remove table", command=donothing)
editmenu.add_separator()
editmenu.add_command(label="Clear tables", command=donothing)
menubar.add_cascade(label="Layout", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

root.mainloop()