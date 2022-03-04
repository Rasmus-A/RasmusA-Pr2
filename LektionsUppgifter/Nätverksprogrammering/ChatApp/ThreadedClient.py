from socket import *
from tkinter import *
import random as rand

wordList = ["ex1", "ex2", "ex3"]

root = Tk()
h = 700
w = 1000
root.geometry("1000x700")
root.resizable(height = False, width = False)
root.title("Chat")

userWindow = Frame(root, width = 250, height = 700, bg = "red")
userWindow.pack(side = LEFT)

chatText = Text(root)
chatText.pack(padx = (0, 107), pady = (600, 0))

sendButton = Button(root,wraplength = 80, height = 6, width = 14, text = "Skicka Meddelande")
sendButton.place(x=893, y=600)

var = StringVar()
myMessages = Message(root, textvariable = var, width = 225)
var.set("cringe")
myMessages.pack(side = RIGHT)


root.mainloop()

def message_handler(myMessageList, otherMessageList):
    pass
"""

def connect_to_server():    # samma som i tidigare exempel
    s = socket()
    host = "localhost"
    port = 12345
    s.connect((host, port))
    return s
conn = connect_to_server()
b = conn.recv(1024)
msg = b.decode('utf-16')
print(msg)

while True:
    msg = input("Skriv något till servern:")
    b = msg.encode("utf-16")
    conn.send(b)
    b = conn.recv(1024)
    msg = b.decode("utf-16")
    print(msg)
"""