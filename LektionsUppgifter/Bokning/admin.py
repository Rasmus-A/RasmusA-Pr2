from socket import *
from _thread import *
from tkinter import *
from tkinter.ttk import Combobox

def connect_to_server():
    s = socket()
    host = "localhost"
    port = 12345
    s.connect((host, port))
    s.sendall
    return s
conn = connect_to_server()



def addRoute():
    pass

def editRoute():
    pass

def deleteRoute():
    pass

def fetchRouteInfo():
    pass

root = Tk()
#root.minsize(200, 300)


# root content
addRouteFrame = Frame(root)
editRouteFrame = Frame(root)
deleteRouteFrame = Frame(root)
mainmenu = Menu(root)

# root layout
addRouteFrame.grid(row=1, column=0, sticky='nsew')
editRouteFrame.grid(row=1, column=1, sticky='nsew')
editRouteFrame.grid(row=1, column=2, sticky='nsew')

def addRouteWindow():
    # addRoute content
    addRouteLabel = Label(addRouteFrame, text='Add route:')
    originLabel = Label(addRouteFrame, text='Origin:')
    destinationLabel = Label(addRouteFrame, text='Destination:')
    methodLabel = Label(addRouteFrame, text='Method of travel:')
    distanceLabel = Label(addRouteFrame, text='Distance:')
    priceLabel = Label(addRouteFrame, text='Price:')

    originEntry = Entry(addRouteFrame)
    destinationEntry = Entry(addRouteFrame)
    methodComboBox = Combobox(addRouteFrame, values=["Bus", "Train", "Airplane", "Boat"])
    distanceEntry = Entry(addRouteFrame)
    priceEntry = Entry(addRouteFrame)
    createButton = Button(addRouteFrame, text='Create route', command=lambda:addRoute())

    # addRoute Layout
    addRouteLabel.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0,5))

    originLabel.grid(row=1, column=0, sticky='ew', pady=(0,5))
    originEntry.grid(row=2, column=0, sticky='ew', padx=5, pady=(0,5))

    destinationLabel.grid(row=1, column=1, sticky='ew', pady=(0,5))
    destinationEntry.grid(row=2, column=1, sticky='ew', padx=5, pady=(0,5))

    methodLabel.grid(row=3, column=0, sticky='e', pady=(0,5))
    methodComboBox.grid(row=3, column=1, sticky='ew', padx=5, pady=(0,5))
    methodComboBox.set("Method of travel")

    distanceLabel.grid(row=4, column=0, sticky='e', pady=(0,5))
    distanceEntry.grid(row=4, column=1, sticky='ew', padx=5, pady=(0,5))

    priceLabel.grid(row=5, column=0, sticky='e', pady=(0,5))
    priceEntry.grid(row=5, column=1, sticky='ew', padx=5, pady=(0,5))

    createButton.grid(row=6, column=0, columnspan=2, sticky='ew', padx=5, pady=(15,5))

def editRouteWindow():
    # addRoute content
    editRouteLabel = Label(addRouteFrame, text='Add route:')
    originLabel = Label(addRouteFrame, text='Origin:')
    destinationLabel = Label(addRouteFrame, text='Destination:')
    methodLabel = Label(addRouteFrame, text='Method of travel:')
    distanceLabel = Label(addRouteFrame, text='Distance:')
    priceLabel = Label(addRouteFrame, text='Price:')

    originEntry = Entry(addRouteFrame)
    destinationEntry = Entry(addRouteFrame)
    methodComboBox = Combobox(addRouteFrame, values=["Bus", "Train", "Airplane", "Boat"])
    distanceEntry = Entry(addRouteFrame)
    priceEntry = Entry(addRouteFrame)
    applyButton = Button(addRouteFrame, text='Create route', command=lambda:addRoute())
    cancelButton = Button(addRouteFrame, textd='Cancel', command=editRouteWindow)

    # editRoute content
    editRouteLabel.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0,5))

    originLabel.grid(row=1, column=0, sticky='ew', pady=(0,5))
    originEntry.grid(row=2, column=0, sticky='ew', padx=5, pady=(0,5))
    originEntry.insert(0, fetchRouteInfo('origin', 'id', id))

    destinationLabel.grid(row=1, column=1, sticky='ew', pady=(0,5))
    destinationEntry.grid(row=2, column=1, sticky='ew', padx=5, pady=(0,5))
    destinationEntry.insert(0, fetchRouteInfo('destination', 'id', id))

    methodLabel.grid(row=3, column=0, sticky='e', pady=(0,5))
    methodComboBox.grid(row=3, column=1, sticky='ew', padx=5, pady=(0,5))
    methodComboBox.set(fetchRouteInfo('method', 'id', id))

    distanceLabel.grid(row=4, column=0, sticky='e', pady=(0,5))
    distanceEntry.grid(row=4, column=1, sticky='ew', padx=5, pady=(0,5))
    distanceEntry.insert(0, fetchRouteInfo('distance', 'id', id))

    priceLabel.grid(row=5, column=0, sticky='e', pady=(0,5))
    priceEntry.grid(row=5, column=1, sticky='ew', padx=5, pady=(0,5))
    priceEntry.insert(0, fetchRouteInfo('price', 'id', id))

    applyButton.grid(row=6, column=0, columnspan=2, sticky='ew', padx=5, pady=(15,5))

def deleteRouteWindow():
    pass

# menu
mainmenu.add_command(label="Add route", command=addRouteWindow)
mainmenu.add_command(label="Edit route", command=editRouteWindow)
mainmenu.add_command(label="Delete route", command=deleteRouteWindow)
root.config(menu=mainmenu)
root.mainloop()