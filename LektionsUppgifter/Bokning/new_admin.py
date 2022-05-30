from socket import *
from _thread import *
from tkinter import *
from tkinter.ttk import Combobox
import mysql.connector
import sys

from pyparsing import col

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='prog2'
)
mycursor = mydb.cursor()

class Route:
    _registry = []

    def __init__(self, ID):
        self._registry.append(self)
        self._ID = ID
        self._origin, self._destination, self._method, self._distance, self._price = self.readRouteFromDatabase()
        self._bookedUsers = self.usersBookedForRoute()
        print('i live')
    
    def remove(self):
        try:
            self._registry.remove(self) # om jag har förstått det rätt så är det här sista referensen till objektet och python slänger det därför helt
        except:
            print(sys.exc_info())
            msgHandler("Server De-sync, please restart client")

    def deleteSelf(self):
        try:
            sql = f"""
                    DELETE 
                        routes, 
                        bookings 
                    FROM 
                        routes 
                    INNER JOIN 
                        bookings 
                    ON 
                        routes.routeID = bookings.routeID 
                    WHERE 
                        routes.routeID = {self._ID}
                    ;"""
            mycursor.execute(sql)
            mydb.commit()
            updater()
            self.remove()
        except:
            print(sys.exc_info())
            msgHandler("Server De-sync, please restart client")

    def readRouteFromDatabase(self):
        try:
            sql = f"""
                    SELECT 
                        origin, 
                        destination, 
                        method, 
                        distance, 
                        price 
                    FROM 
                        routes 
                    WHERE 
                        routeID = {self._ID}
                    ;"""
            mycursor.execute(sql)
            routeData = mycursor.fetchall()
            return routeData[0] # kommer i en lista
        except:
            print(sys.exc_info())
            msgHandler("Server De-sync, please restart client")

    def checkForDuplicate(self, new_origin, new_destination, new_method):
        try:
            sql = f""" 
                    SELECT EXISTS(
                        SELECT 
                            * 
                        FROM 
                            routes 
                        WHERE 
                            origin = '{new_origin}' 
                            AND 
                            destination = '{new_destination}' 
                            AND 
                            method = '{new_method}' 
                            AND NOT
                            routeID = {self._ID})
                        ;"""
            mycursor.execute(sql)
            duplicate = mycursor.fetchall()[0][0] # svar ges i en lista
            duplicate = bool(duplicate) #0/1 -> False/True
            return duplicate
        except:
            msgHandler("Server De-sync, please restart client")
            return None

    def updateDatabase(self, new_origin, new_destination, new_method, new_distance, new_price):
        try:
            sql = f"""
                    UPDATE 
                        routes 
                    SET 
                        origin = '{new_origin}', 
                        destination = '{new_destination}', 
                        method = '{new_method}', 
                        distance = '{new_distance}', 
                        price = '{new_price}' 
                    WHERE 
                        routeID = {self._ID}
                    ;"""
            mycursor.execute(sql)
            mydb.commit()
            updater()
        except:
            print(sys.exc_info())
            msgHandler("Server De-sync, please restart client")

    def usersBookedForRoute(self):
        try:
            # tar fram namn och ID för all användare bokade på en viss route
            sql = f"""
                    SELECT 
                        firstname, 
                        lastname, 
                        users.userID 
                    FROM 
                        users 
                    INNER JOIN 
                        bookings 
                    ON 
                        users.userID = bookings.UserID 
                    WHERE 
                        routeID = {self._ID}
                    ;"""
            mycursor.execute(sql)
            users = mycursor.fetchall()
            return users
        except:
            print(sys.exc_info())
            msgHandler("Server De-sync, please restart client")

    def removeUsers(self, userIndex):
        #try:
        usersToRemoveID = []
        for i in userIndex:
            usersToRemoveID.append(self._bookedUsers[i][2]) # tar fram användar IDn utifrån användarnas plats i listan över bokade på denna route
        for u in usersToRemoveID:
            sql = f"""
                    DELETE FROM 
                        bookings 
                    WHERE 
                        routeID = {self._ID} 
                        AND 
                        userID = {u}
                    ;"""
            mycursor.execute(sql)
            mydb.commit()
        updater()
        #except:
            #print(sys.exc_info())
            #msgHandler("Server De-sync, please restart client")

    def getID(self):
        return self._ID

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

    def getUsers(self):
        return self._bookedUsers  

class RouteOnSurface(Route):
    def __init__(self, ID):
        super().__init__(ID)

class RouteInAir(Route):
    def __init__(self, ID):
        super().__init__ (ID)

class BusRoute(RouteOnSurface):
    def __init__(self, ID):
        super().__init__(ID)

class TrainRoute(RouteOnSurface):
    def __init__(self, ID):
        super().__init__(ID)

class BoatRoute(RouteOnSurface):
    def __init__(self, ID):
        super().__init__(ID)

class AirplaneRoute(RouteInAir):
    def __init__(self, ID):
        super().__init__(ID)

def updater():
    for R in Route._registry: # raderar alla route obj ur registry
        print(R)
        R.remove()
    # initialiserar nya obj utifrån databas
    try:    
        sql = """
                SELECT 
                    routeID, 
                    method 
                FROM 
                    routes
                ;"""
        mycursor.execute(sql)
        routes = mycursor.fetchall()

        for r in range(len(routes)):
            ID = routes[r][0]
            if routes[r][1] == 'Bus':
                ID = BusRoute(ID)
            elif routes[r][1] == 'Train':
                ID = TrainRoute(ID)
            elif routes[r][1] == 'Boat':
                ID = BoatRoute(ID)
            elif routes[r][1] == 'Airplane':
                ID = AirplaneRoute(ID)
    except:
        msgHandler("Server De-sync, please restart client")
    addRouteFrame.grid_forget()
    bookingsFrame.grid_forget()
    editRouteFrame.grid_forget()
    addRouteFrame.grid()
    addRouteWindow()

# Ger False om något inputfält är tomt
def validateInput(*input): 
    for i in input:
        if not i:
            return False
    return True

def msgHandler(msg):
    def OKButtonHandler():
        msg_popup.destroy()
        if msg == "Server De-sync, please restart client" or msg == "Fatal error, please restart client":
            exit()
        else:
            updater()

    msg_popup = Toplevel()
    msg_popup.resizable(width=FALSE, height=FALSE)
    msg_popup.title("Alert")
    msgLabel = Label(msg_popup, text=msg, wraplength=100)
    msgButton = Button(msg_popup, text="OK", command=OKButtonHandler)

    msgLabel.grid(row=0, column=0, sticky='ew', pady=(5,15))
    msgButton.grid(row=1, column=0, pady=(0,10))


# Ger alla bokningsbara rutter i ett format som är lättare att läsa och ett dictionary för att hitta tillbaka till objektet
def activeRoutes(): 
    editable = [] 
    editableIndex = {}
    for R in Route._registry:
        print(f"active: {R}")
        readableStr = f"{R.getOrigin()} -> {R.getDestination()} by {R.getMethod()}"
        editableIndex[readableStr] = R
        editable.append(readableStr)
    return editable, editableIndex

root = Tk()
root.resizable(width=FALSE, height=FALSE)

# root content
addRouteFrame = Frame(root)
editRouteFrame = Frame(root)
deleteRouteFrame = Frame(root)
bookingsFrame = Frame(root)
bookingsFrameSub = Frame(bookingsFrame)
mainmenu = Menu(root)

def addRouteWindow():
    def createButton_pressed(): # hanterar, validerar, och skapar ny rutt vid knapptryck
        try:
            origin = originEntry.get()
            destination = destinationEntry.get()
            method = methodComboBox.get()
            distance = int(distanceEntry.get())
            price = int(priceEntry.get())
        except:
            msgHandler("Invalid Input")

        valid = validateInput(origin, destination, method, distance, price)

        if valid == False:
            msgHandler("Invalid Input")
        else:
            # kollar efter dubbletter i databas
            sql = f"""
                    SELECT EXISTS(
                        SELECT 
                            * 
                        FROM 
                            routes 
                        WHERE 
                            origin = '{origin}' 
                            AND 
                            destination = '{destination}' 
                            AND
                            method = '{method}')
                        ;"""
            mycursor.execute(sql)
            duplicate = mycursor.fetchall()[0][0] # svar ges i en lista och tuple
            duplicate = bool(duplicate) #0/1 -> False/True

            if duplicate == True:
                msgHandler("Duplicate/Already exists")

            elif valid == True and duplicate == False:
                try:
                    sql = """
                            INSERT 
                            INTO 
                                routes 
                                    (origin, 
                                    destination, 
                                    method, 
                                    distance, 
                                    price) 
                            VALUES 
                                (%s, %s, %s, %s, %s)
                            ;"""
                    val = (origin, destination, method, distance, price)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print("created", sql)
                    updater()
                except:
                    msgHandler("Server De-sync, please restart client")
            
            else:
                msgHandler("Fatal error, please restart client")

    # addRoute content
    addRouteLabel = Label(addRouteFrame, text="Add route:")
    originLabel = Label(addRouteFrame, text="Origin:")
    destinationLabel = Label(addRouteFrame, text="Destination:")
    methodLabel = Label(addRouteFrame, text="Method of travel:")
    distanceLabel = Label(addRouteFrame, text="Distance:")
    priceLabel = Label(addRouteFrame, text="Price:")

    originEntry = Entry(addRouteFrame)
    destinationEntry = Entry(addRouteFrame)
    methodComboBox = Combobox(addRouteFrame, values=["Bus", "Train", "Airplane", "Boat"], state='readonly')
    distanceEntry = Entry(addRouteFrame)
    priceEntry = Entry(addRouteFrame)

    createButton = Button(addRouteFrame, text="Create route", command=createButton_pressed)

    # addRoute Layout
    addRouteLabel.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0,5))

    originLabel.grid(row=1, column=0, sticky='ew', pady=(0,5))
    originEntry.grid(row=2, column=0, sticky='ew', padx=5, pady=(0,5))

    destinationLabel.grid(row=1, column=1, sticky='ew', pady=(0,5))
    destinationEntry.grid(row=2, column=1, sticky='ew', padx=5, pady=(0,5))

    methodLabel.grid(row=3, column=0, sticky='e', pady=(0,5))
    methodComboBox.grid(row=3, column=1, sticky='ew', padx=5, pady=(0,5))

    distanceLabel.grid(row=4, column=0, sticky='e', pady=(0,5))
    distanceEntry.grid(row=4, column=1, sticky='ew', padx=5, pady=(0,5))

    priceLabel.grid(row=5, column=0, sticky='e', pady=(0,5))
    priceEntry.grid(row=5, column=1, sticky='ew', padx=5, pady=(0,5))

    createButton.grid(row=6, column=0, columnspan=2, sticky='ew', padx=5, pady=(15,5))

def editRouteWindow():    
    def applyButton_pressed():
        R = editableIndex[editRouteCombobox.get()] # tar fram en vald route R
        try:
            new_origin = originEntry.get()
            new_destination = destinationEntry.get()
            new_method = methodComboBox.get()
            new_distance = int(distanceEntry.get())
            new_price = int(priceEntry.get())
        except:
            msgHandler("Invalid Input")

        valid = validateInput(new_origin, new_destination, new_method, new_distance, new_price)

        if valid == False:
            print("not valid")
            msgHandler("Invalid Input")

        else:
            duplicate = R.checkForDuplicate(new_origin, new_destination, new_method)

            if duplicate == True:
                msgHandler("Duplicate/Already exists")

            elif valid == True and duplicate == False:
                    R.updateDatabase(new_origin, new_destination, new_method, new_distance, new_price)

            else:
                msgHandler("Fatal error, please restart client")
        
    def editButton_pressed(): # tar upp information om vald route vid knapptryck
        R = editableIndex[editRouteCombobox.get()] # tar fram en vald route R

        originEntry.delete(0, END)
        destinationEntry.delete(0, END)
        distanceEntry.delete(0, END)
        priceEntry.delete(0, END)

        originEntry.insert(0, R.getOrigin())
        destinationEntry.insert(0, R.getDestination())
        methodComboBox.set(R.getMethod())
        distanceEntry.insert(0, R.getDistance())
        priceEntry.insert(0, R.getPrice())

    def deleteButton_pressed():
        R = editableIndex[editRouteCombobox.get()] # tar fram en vald route R

        # skapar en popup
        popup_screen = Toplevel()
        popup_screen.title('')
        popup_screen.resizable(width=FALSE, height=FALSE)

        # popup content
        warningLabel = Label(popup_screen, text='Warning!')
        infoLabel = Label(popup_screen, text='You are about to delete a route!')

        continueButton = Button(popup_screen, text='Continue', command=lambda: [R.deleteSelf(), popup_screen.destroy()])
        cancelDeleteButton = Button(popup_screen, text='Cancel', command=popup_screen.destroy)

        # popup layout
        warningLabel.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0,5))
        infoLabel.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0,5))

        continueButton.grid(row=2, column=0, sticky='ew', padx=5, pady=(0,5))
        cancelDeleteButton.grid(row=2, column=1, sticky='ew', padx=5, pady=(0,5))

        # återställer edit skärmen i bakgrunden
        editRouteWindow()

    # editRoute content
    editRouteLabel = Label(editRouteFrame, text='Edit route:')
    originLabel = Label(editRouteFrame, text='Origin:')
    destinationLabel = Label(editRouteFrame, text='Destination:')
    methodLabel = Label(editRouteFrame, text='Method of travel:')
    distanceLabel = Label(editRouteFrame, text='Distance:')
    priceLabel = Label(editRouteFrame, text='Price:')

    editable, editableIndex = activeRoutes()

    editRouteCombobox = Combobox(editRouteFrame, values=editable, state='readonly')
    originEntry = Entry(editRouteFrame)
    destinationEntry = Entry(editRouteFrame)
    methodComboBox = Combobox(editRouteFrame, values=["Bus", "Train", "Airplane", "Boat"], state='readonly')
    distanceEntry = Entry(editRouteFrame)
    priceEntry = Entry(editRouteFrame)

    editRouteButton = Button(editRouteFrame, text='Edit', command=editButton_pressed)
    applyButton = Button(editRouteFrame, text='Apply changes', command=applyButton_pressed)
    
    cancelButton = Button(editRouteFrame, text='Cancel', command=editRouteWindow)
    deleteButton = Button(editRouteFrame, text='Delete Route', command=deleteButton_pressed)

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

def bookedRoutesWindow():
    def showButton_pressed():
        def removeUsersButton_pressed():
            userIndex = usersListbox.curselection() # ger alla valda rader i listbox
            usersListbox.delete(0, END)
            R.removeUsers(userIndex)

        R = editableIndex[showRouteCombobox.get()] # tar fram en vald route R

        for W in bookingsFrameSub.winfo_children(): # tar bort ev. tidigare listbox o tillhörigheter
            W.destroy()

        usersListLabel = Label(bookingsFrameSub, text="Users on booked on this route:")
        usersListbox = Listbox(bookingsFrameSub, selectmode=MULTIPLE)
        removeUsersButton = Button(bookingsFrameSub, text="Remove user(s) from route", command=removeUsersButton_pressed)

        for i in range(len(R.getUsers())): # lägger användarinformation i en listbox
            firstname, lastname, userID = R.getUsers()[i]
            usersListbox.insert(i, f"Name: {firstname} {lastname}, ID: {userID}")

        usersListLabel.grid(row=0, column=0, columnspan=2, stick='ew')
        usersListbox.grid(row=1, column=0, columnspan=2, sticky='ew')
        removeUsersButton.grid(row=2, column=0, columnspan=2)
        
    # content
    showUsersLabel = Label(bookingsFrame, text="See people on:")
    usersLabel = Label(bookingsFrame, text="")

    editable, editableIndex = activeRoutes()
    showRouteCombobox = Combobox(bookingsFrame, values=editable, state='readonly')

    showUsersButton = Button(bookingsFrame, text="Show", command=showButton_pressed)
    
    # layout
    showUsersLabel.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0,5))
    
    showRouteCombobox.grid(row=1, column=0, sticky='ew', padx=5, pady=(0,5))
    showUsersButton.grid(row=1, column=1, sticky='ew', padx=5, pady=(0,5))

    usersLabel.grid(row=2, column=0, columnspan=2, sticky='ew')
    bookingsFrameSub.grid(row=3, column=0, columnspan=2, sticky='ew')

mainmenu.add_command(label="Add route", command=lambda:[editRouteFrame.grid_forget(),
                                                         bookingsFrame.grid_forget(), 
                                                         addRouteFrame.grid(), 
                                                         addRouteWindow()]
                                                         )
mainmenu.add_command(label="Edit route", command=lambda:[addRouteFrame.grid_forget(), 
                                                         bookingsFrame.grid_forget(), 
                                                         editRouteFrame.grid(), 
                                                         editRouteWindow()]
                                                         )
mainmenu.add_command(label="See booked routes", command=lambda:[addRouteFrame.grid_forget(), 
                                                               editRouteFrame.grid_forget(), 
                                                               bookingsFrame.grid(), 
                                                               bookedRoutesWindow()]
                                                               )

root.config(menu=mainmenu)

#start_new_thread(updateListener, (conn, ))
print(sys.exc_info())
updater()

addRouteFrame.grid()
addRouteWindow()

root.mainloop()