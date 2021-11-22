from tkinter import *
root = Tk()
var = StringVar()
label = Label(root, textvariable=var, relief=RAISED)
var.set("wow")
label.pack()
root.mainloop()