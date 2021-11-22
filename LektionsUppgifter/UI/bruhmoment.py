import ctypes
from tkinter import *
root = Tk()
MessageBox = ctypes.windll.user32.MessageBoxW
b = Button(root, text ="BRUHMOMENT")
def bruhmomentExecutor(self):
    MessageBox(None, 'bruhmoment detected', 'bruhmoment detector', 0)
b.bind("<Button-1>", bruhmomentExecutor)
b.pack()
root.mainloop()



