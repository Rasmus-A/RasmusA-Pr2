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

class Route:
    _registry = []

    def __init__(self, id):
        self._registry.append(self)
        self._id = id
        self.getRoute()
        self._active = True  # Som jag förstår det är 'del' inte ett pålitligt sätt att radera objekt, de här e en halvdum workaround
        print('i live')
    
    def getRoute(self):
        self._origin = fetchItemInfo('origin', 'routes', 'id', self._id)[0]
        self._destination = fetchItemInfo('destination', 'routes', 'id', self._id)[0]
        self._method = fetchItemInfo('method', 'routes', 'id', self._id)[0]
        self._distance = int(fetchItemInfo('distance', 'routes', 'id', self._id)[0])
        self._price = int(fetchItemInfo('price', 'routes', 'id', self._id)[0])
    
    def updateRoute(self):
        instructions = ",".join(map(str, [
            3,
            self._origin,
            self._destination,
            self._method,
            self._distance,
            self._price,
            self._id
            ])).encode('utf-8')
        conn.send(instructions)

    def deleteRoute(self):
        instructions = ",".join(map(str, [
            4,
            'routes',
            'id',
            self._id
            ])).encode('utf-8')
        self._registry.remove(self)
        self._active = False
        conn.send(instructions)

    def getID(self):
        return self._id

    def getOrigin(self):
        return self._origin
    
    def getDestination(self):
        return self._destination
    
    def getMethod(self):
        return self._method

    def getDistance(self):
        return self._distance

    def getPrice(self):
        return self._price

    def getActive(self):
        return self._active
    
    def setOrigin(self, newOrigin):
        self._origin = newOrigin

    def setDestination(self, newDestination):
        self._destination = newDestination

    def setDistance(self, newDistance):
        self._distance = int(newDistance)

    def setPrice(self, newPrice):
        self._price = int(newPrice)

    def setMethod(self, newMethod):
        addRoute(self._origin, self._destination, newMethod, self._distance, self._price)
        self.deleteRoute()

class RouteOnSurface(Route):
    def __init__(self, id):
        super().__init__(id)
        self._paymentInAdvance = False

class RouteInAir(Route):
    def __init__(self, id):
        super().__init__ (id)
        self._paymentIndAdvance = True

class BusRoute(RouteOnSurface):
    def __init__(self, id):
        super().__init__(id)

class TrainRoute(RouteOnSurface):
    def __init__(self, id):
        super().__init__(id)

class BoatRoute(RouteOnSurface):
    def __init__(self, id):
        super().__init__(id)

class AirplaneRoute(RouteInAir):
    def __init__(self, id):
        super().__init__(id)

def createRouteObj(id):
    method = fetchItemInfo('method', 'routes', 'id', id)
    print(method)
    if method[0] == 'Bus':
        id = BusRoute(id)
    elif method[0] == 'Train':
        id = TrainRoute(id)
    elif method[0] == 'Boat':
        id = BoatRoute(id)
    elif method[0] == 'Airplane':
        id = AirplaneRoute(id)

def addRoute(origin, destination, method, distance, price):
    print(origin, destination, method, distance, price)
    instructions = ",".join(map(str, [1, origin, destination, method, distance, price])).encode('utf-8')
    conn.send(instructions)
    id = fetchItemInfo('id', 'routes')[-1]
    createRouteObj(id)

# fetchItemInfo finns som en egen metod utanför klasser för att fallen där den behövs är mycket olika och den behövs innan en klass har initialiserats
def fetchItemInfo(*request):   # request på formen SELECT (sökt information) FROM (table) /WHERE (kolumnnamn) = (värde)/
    instructions =  [5]
    for i in request:
        instructions.append(i)
    instructions = ",".join(map(str, instructions))
    instructions = instructions.encode('utf-8')
    conn.send(instructions)
    answer = conn.recv(1024).decode('utf-8')
    answer = answer.split(",")
    return answer

# root configurering
root = Tk()
root.resizable(width=FALSE, height=FALSE)

# root content
addRouteFrame = Frame(root)
editRouteFrame = Frame(root)
deleteRouteFrame = Frame(root)
mainmenu = Menu(root)

# root layout


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

    createButton = Button(addRouteFrame, text='Create route', command=lambda:addRoute(
        originEntry.get(), 
        destinationEntry.get(), 
        methodComboBox.get(), 
        distanceEntry.get(), 
        priceEntry.get())
        )

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
    def showRoute(R):
        originEntry.delete(0, END)
        destinationEntry.delete(0, END)
        distanceEntry.delete(0, END)
        priceEntry.delete(0, END)

        originEntry.insert(0, R.getOrigin())
        destinationEntry.insert(0, R.getDestination())
        methodComboBox.set(R.getMethod())
        distanceEntry.insert(0, R.getDistance())
        priceEntry.insert(0, R.getPrice())

    def setRoute(R, origin, destination, method, distance, price):
        print(R, origin, destination, method, distance, price)
        R.setOrigin(origin)
        R.setDestination(destination)
        R.setDistance(distance)
        R.setPrice(price)
        R.updateRoute()        
        if method != R.getMethod():
            R.setMethod(method)


    def safetyPopup(R):
        popup_screen = Toplevel()
        popup_screen.title('')
        popup_screen.resizable(width=FALSE, height=FALSE)

        # popup content
        warningLabel = Label(popup_screen, text='Warning!')
        infoLabel = Label(popup_screen, text='You are about to delete a Route!')

        continueButton = Button(popup_screen, text='Continue', command=R.deleteRoute)
        cancelDeleteButton = Button(popup_screen, text='Cancel', command=popup_screen.destroy)

        # popup layout
        warningLabel.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0,5))
        infoLabel.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0,5))

        continueButton.grid(row=2, column=0, sticky='ew', padx=5, pady=(0,5))
        cancelDeleteButton.grid(row=2, column=1, sticky='ew', padx=5, pady=(0,5))
        #continueButton.config(state=DISABLED)
        #root.after(2000, continueButton.config(state=NORMAL))

    # editRoute content
    editRouteLabel = Label(editRouteFrame, text='Edit route:')
    originLabel = Label(editRouteFrame, text='Origin:')
    destinationLabel = Label(editRouteFrame, text='Destination:')
    methodLabel = Label(editRouteFrame, text='Method of travel:')
    distanceLabel = Label(editRouteFrame, text='Distance:')
    priceLabel = Label(editRouteFrame, text='Price:')

    editable = [] 
    editableIndex = {}
    for R in Route._registry:
        readableStr = f"{R.getOrigin()} -> {R.getDestination()} by {R.getMethod()}"
        editableIndex[readableStr] = R
        editable.append(readableStr)
            
    editRouteCombobox = Combobox(editRouteFrame, values=editable)
    originEntry = Entry(editRouteFrame)
    destinationEntry = Entry(editRouteFrame)
    methodComboBox = Combobox(editRouteFrame, values=["Bus", "Train", "Airplane", "Boat"])
    distanceEntry = Entry(editRouteFrame)
    priceEntry = Entry(editRouteFrame)

    editRouteButton = Button(editRouteFrame, text='Edit', command=lambda:showRoute(editableIndex[editRouteCombobox.get()]))
    applyButton = Button(editRouteFrame, text='Apply changes', command=lambda:[setRoute(
        editableIndex[editRouteCombobox.get()],
        originEntry.get(),
        destinationEntry.get(),
        methodComboBox.get(),
        distanceEntry.get(),
        priceEntry.get()
        ),
        editRouteWindow()]
        )
    
    cancelButton = Button(editRouteFrame, text='Cancel', command=editRouteWindow)
    deleteButton = Button(editRouteFrame, text='Delete Route', command=lambda:safetyPopup(editableIndex[editRouteCombobox.get()]))

    # editRoute layout
    editRouteLabel.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0,5))

    editRouteCombobox.grid(row=1, column=0, sticky='ew', padx=5, pady=(0,5))
    editRouteButton.grid(row=1, column=1, sticky='ew', padx=5, pady=(0,5))

    originLabel.grid(row=2, column=0, sticky='ew', pady=(0,5))
    originEntry.grid(row=3, column=0, sticky='ew', padx=5, pady=(0,5))
    

    destinationLabel.grid(row=2, column=1, sticky='ew', pady=(0,5))
    destinationEntry.grid(row=3, column=1, sticky='ew', padx=5, pady=(0,5))
    

    methodLabel.grid(row=4, column=0, sticky='e', pady=(0,5))
    methodComboBox.grid(row=4, column=1, sticky='ew', padx=5, pady=(0,5))


    distanceLabel.grid(row=5, column=0, sticky='e', pady=(0,5))
    distanceEntry.grid(row=5, column=1, sticky='ew', padx=5, pady=(0,5))


    priceLabel.grid(row=6, column=0, sticky='e', pady=(0,5))
    priceEntry.grid(row=6, column=1, sticky='ew', padx=5, pady=(0,5))


    applyButton.grid(row=7, column=0, sticky='ew', padx=5, pady=(15,5))
    deleteButton.grid(row=7, column=1, sticky='ew', padx=5, pady=(15,5))
    cancelButton.grid(row=8, column=0, columnspan=2, sticky='ew', padx=5, pady=(0,5))

def startUp():
    for id in fetchItemInfo('id', 'routes'):
        print("hej")
        createRouteObj(id)



#addRouteFrame.grid(row=1, column=0, sticky='nsew')
#editRouteFrame.grid(row=1, column=1, sticky='nsew')

#getRoutes()
# menu
mainmenu.add_command(label="Add route", command=lambda:[editRouteFrame.grid_forget(), addRouteFrame.grid(), addRouteWindow()])
mainmenu.add_command(label="Edit route", command=lambda:[addRouteFrame.grid_forget(), editRouteFrame.grid(), editRouteWindow()])
root.config(menu=mainmenu)

startUp()

root.mainloop()