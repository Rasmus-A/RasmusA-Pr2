from tkinter import *
import hashlib
from socket import *
from _thread import *
import mysql.connector
import sys

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
        self._paymentInAdvance = None
        self._time = None
        print('i live')
    
    def remove(self):
        try:
            self._registry.remove(self) # om jag har förstått det rätt så är det här sista referensen till objektet och python slänger det därför helt
        except:
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
            msgHandler("Server De-sync, please restart client")

    def bookRoute(self, userID):
        try:
            sql = f"SELECT EXISTS(SELECT * FROM bookings WHERE userID = '{userID}' AND routeID = '{self._ID}');"
            mycursor.execute(sql)
            duplicate = mycursor.fetchall()[0][0] # svar ges i en lista
            duplicate = bool(duplicate) #0/1 -> False/True
        except:
            msgHandler("Server De-sync, please restart client")

        if duplicate == False:
            try:
                sql = """INSERT INTO bookings VALUES (%s, %s);"""
                val = (userID, self._ID)
                mycursor.execute(sql, val)
                mydb.commit()
                updater()
            except:
                msgHandler("Server De-sync, please restart client")
        else:
            msgHandler("You have aready booked this route")   

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

    def getTime(self):
        return self._time

    def getPayment(self):
        return self._paymentInAdvance

class RouteOnSurface(Route):
    def __init__(self, ID):
        super().__init__(ID)
        self._paymentInAdvance = "on location"

class RouteInAir(Route):
    def __init__(self, ID):
        super().__init__ (ID)
        self._paymentInAdvance = "before departure, by email"  # Det är här man skulle ha använt smtplib o ssl för att skicka ett litet mail men jag orkar inte o

class BusRoute(RouteOnSurface):
    def __init__(self, ID):
        super().__init__(ID)
        self._time = (f"{self._distance//80} Hours, {round(((self._distance/80)%1)*60, 0)} Minutes")

class TrainRoute(RouteOnSurface):
    def __init__(self, ID):
        super().__init__(ID)
        self._time = (f"{self._distance//200} Hours, {round(((self._distance/200)%1)*60, 0)} Minutes")

class BoatRoute(RouteOnSurface):
    def __init__(self, ID):
        super().__init__(ID)
        self._time = (f"{self._distance//45} Hours, {round(((self._distance/45)%1)*60, 0)} Minutes")

class AirplaneRoute(RouteInAir):
    def __init__(self, ID):
        super().__init__(ID)
        self._time = (f"{self._distance//900} Hours, {round(((self._distance/900)%1)*60, 0)} Minutes")

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
        elif msg == "Invalid Input" or msg == "Incorrect username or password":
            registerScreen()
        
    msg_popup = Toplevel()
    msg_popup.resizable(width=FALSE, height=FALSE)
    msg_popup.title("Alert")
    msgLabel = Label(msg_popup, text=msg, wraplength=100)
    msgButton = Button(msg_popup, text="OK", command=OKButtonHandler)

    msgLabel.grid(row=0, column=0, sticky='ew', pady=(5,15))
    msgButton.grid(row=1, column=0, pady=(0,10))

root = Tk()

def registerScreen():
    def registerButton_pressed():
        firstname = firstNameEntry.get()
        lastname = lastNameEntry.get()
        email = emailEntry.get()
        username = usernameEntry.get()
        password = hashlib.sha256(passwordEntry.get().encode('utf-8')).hexdigest()

        valid = validateInput(firstname, lastname, email, username, password)

        if valid == False:
            msgHandler("Invalid Input")
        else:
            exists = None
            try: # kolla efter tagna usernames
                print("Hej från register dup")
                sql = f"""SELECT EXISTS(SELECT * FROM users WHERE username = '{username}');"""
                mycursor.execute(sql)
                exists = mycursor.fetchall()[0][0] # svar ges i en lista och tuple
                exists = bool(exists) #0/1 -> False/True
                print(exists)
            except:
                msgHandler("Username already taken")

            if exists == False:
                try:
                    sql = """INSERT INTO users (firstname, lastname, email, username, password) VALUES (%s, %s, %s, %s, %s);"""
                    val = (firstname, lastname, email, username, password)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    updater()
                    root.deiconify()
                    register_screen.withdraw()
                    mainScreen(password)
                except:
                    msgHandler("Server De-sync, please restart client")
            else:
                msgHandler("Fatal error, please restart client")


    global registerErrorLabel, register_screen
    # Register screen content
    register_screen = Toplevel()
    register_screen.title('Register')
    register_screen.resizable(height = False, width = False)

    firstNameLabel = Label(register_screen, text='First name:')
    lastNameLabel = Label(register_screen, text='Last name:')
    emailLabel = Label(register_screen, text='E-mail address:')
    usernameLabel = Label(register_screen, text='Username:')
    passwordLabel = Label(register_screen, text='Password:')
    registerErrorLabel = Label(register_screen, text=' ')   
    signInLabel = Label(register_screen, text='Already a member?')

    firstNameEntry = Entry(register_screen)
    lastNameEntry = Entry(register_screen)
    emailEntry = Entry(register_screen)
    usernameEntry = Entry(register_screen)
    passwordEntry = Entry(register_screen, show='*')

    showPasswordButton = Button(register_screen, text="S", command=lambda:[
        passwordEntry.config(show=''),
        showPasswordButton.grid_forget(),
        hidePasswordButton.grid(row=9, column=3, sticky='ew', padx=(0,5), pady=(0,20))
        ])
    hidePasswordButton = Button(register_screen, text="H", command=lambda:[
        passwordEntry.config(show='*'),
        hidePasswordButton.grid_forget(),
        showPasswordButton.grid(row=9, column=3, sticky='ew', padx=(0,5), pady=(0,20))
        ])
    registerButton = Button(register_screen,text='Register', command=registerButton_pressed)
    signInButton = Button(register_screen, text='Sign in here!', command=lambda: [signInScreen(), register_screen.withdraw()])

    # Register screen layout
    firstNameLabel.grid(row=0, column=0, columnspan=4, sticky='ew', pady=(5,0))
    firstNameEntry.grid(row=1, column=0, columnspan=4, sticky='ew', padx=5, pady=(0,5))

    lastNameLabel.grid(row=2, column=0, columnspan=4, sticky='ew', pady=(0,5))
    lastNameEntry.grid(row=3, column=0, columnspan=4, sticky='ew', padx=5, pady=(0,5))

    emailLabel.grid(row=4, column=0, columnspan=4, sticky='ew', pady=(0,5))
    emailEntry.grid(row=5, column=0, columnspan=4, sticky='ew', padx=5, pady=(0,5))



    usernameLabel.grid(row=6, column=0, columnspan=4, sticky='ew', pady=(0,5))
    usernameEntry.grid(row=7, column=0, columnspan=4, sticky='ew', padx=5, pady=(0,5))

    passwordLabel.grid(row=8, column=0, columnspan=4, sticky='ew', pady=(0,5))
    passwordEntry.grid(row=9, column=0, columnspan=3, sticky='ew', padx=(5,0), pady=(0,20))
    showPasswordButton.grid(row=9, column=3, sticky='ew', padx=(0,5), pady=(0,20))

    registerButton.grid(row=10, column=0, columnspan=4, sticky='ew', padx=5, pady=(0,5))

    registerErrorLabel.grid(row=11, column=0, sticky='ew', padx=5, pady=(0,35))

    signInLabel.grid(row=12, column=0, columnspan=4, sticky='ew', padx=5, pady=(0,5))
    signInButton.grid(row=13, column=0, columnspan=4, sticky='ew', padx=5, pady=(0,5))

def signInScreen():
    def signInButton_pressed():
        username = usernameEntry.get()
        password = hashlib.sha256(passwordEntry.get().encode('utf-8')).hexdigest()
        truePassword = None

        valid = validateInput(username, password)

        if valid == False:
            msgHandler("Invalid Input")

        else:
            exists = ""
            try:
                sql = f"""SELECT EXISTS(SELECT * FROM users WHERE username = '{username}');"""
                mycursor.execute(sql)
                exists = mycursor.fetchall()[0][0] # svar ges i en lista och tuple
                print(exists)
                exists = bool(exists) #0/1 -> False/True
            except:
                msgHandler("Server De-sync, please restart client")
            
            if exists == True:
                try:
                    sql = f"""SELECT password FROM users WHERE username = '{username}';"""
                    mycursor.execute(sql)
                    truePassword = mycursor.fetchall()[0][0] # svar ges i en lista och tuple
                    print(truePassword)
                except:
                    msgHandler("Server De-sync, please restart client")
            else:
                msgHandler("Incorrect username or password")
            
            if password == truePassword:
                root.deiconify()
                signIn_screen.withdraw()
                mainScreen(password)
            else:
                msgHandler("Incorrect username or password")


    global signInErrorLabel, signIn_screen
    # Sign in screen content
    signIn_screen = Toplevel()
    signIn_screen.title('Sign In')
    signIn_screen.resizable(height = False, width = False)

    usernameLabel = Label(signIn_screen, text='Username:')
    passwordLabel = Label(signIn_screen, text='Password:')
    signInErrorLabel = Label(signIn_screen, text=' ')       
    registerLabel = Label(signIn_screen, text='Not a member?')

    usernameEntry = Entry(signIn_screen)
    passwordEntry = Entry(signIn_screen, show='*')

    showPasswordButton = Button(signIn_screen, text="S", command=lambda:[
        passwordEntry.config(show=''),
        showPasswordButton.grid_forget(),
        hidePasswordButton.grid(row=3, column=3, sticky='ew', padx=(0,5), pady=(0,20))
        ])
    hidePasswordButton = Button(signIn_screen, text="H", command=lambda:[
        passwordEntry.config(show='*'),
        hidePasswordButton.grid_forget(),
        showPasswordButton.grid(row=3, column=3, sticky='ew', padx=(0,5), pady=(0,20))
        ])
    signInButton = Button(signIn_screen, text='Login', command=signInButton_pressed)
    registerButton = Button(signIn_screen, text='Register here!', command=lambda: [registerScreen(), signIn_screen.withdraw()])

    # Sign in screen layout
    usernameLabel.grid(row=0, column=0, columnspan=4, sticky='ew', pady=(5,0))
    usernameEntry.grid(row=1, column=0, columnspan=4, sticky='ew', padx=5, pady=(0,5))

    passwordLabel.grid(row=2, column=0, columnspan=4, sticky='ew')
    passwordEntry.grid(row=3, column=0, columnspan=3, sticky='ew', padx=(5,0), pady=(0,20))
    showPasswordButton.grid(row=3, column=3, sticky='ew', padx=(0,5), pady=(0,20))

    signInButton.grid(row=5, column=0, columnspan=4, sticky='ew', padx=5, pady=(0,5))
    signInErrorLabel.grid(row=6, column=0, columnspan=4, sticky='ew', pady=(0,35))

    registerLabel.grid(row=7, column=0, columnspan=4, sticky='ew', padx=5, pady=(0,5))
    registerButton.grid(row=8, column=0, columnspan=4, sticky='ew', padx=5, pady=(0,5))

def mainScreen(password):
    # hitta userID
    sql = f"""SELECT userID from users WHERE password = '{password}';"""
    mycursor.execute(sql)
    userID = mycursor.fetchall()[0][0]

    def displayAvailibleRoutes(selected_method):
        print("hej från disp")
        updater()
        for W in contentFrame.winfo_children():
            W.destroy()
        for W in routeFrame.winfo_children():
            print(W)
            W.destroy()
        rowCount = 0
        for R in Route._registry:
            print("hej")
            if R.getMethod() == selected_method:
                print("im in")
                readableStr = f'{R.getOrigin()} -> {R.getDestination()}'
                buttonID = Button(routeFrame, text=readableStr, command=lambda R=R:showSelectedRoute(R), width=10, wraplength=80)
                buttonID.grid(row=rowCount, column=0, sticky='ew')
                rowCount += 1

    def showSelectedRoute(R):
        for W in contentFrame.winfo_children():
            W.destroy()

        journeyLabel = Label(contentFrame, text=f"From {R.getOrigin()} To {R.getDestination()}")
        timeLabel = Label(contentFrame, text=f"Est. Travel Time: {R.getTime()}")
        infoLabel = Label(contentFrame, text=f"Full cost is to be payed {R.getPayment()}")
        
        bookButton = Button(contentFrame, text=f"Book now for only: {R.getPrice()}", command=lambda: R.bookRoute(userID))

        journeyLabel.grid(row=0, column=0, columnspan=3, sticky='ew', padx=40, pady=(20,10))
        timeLabel.grid(row=1, column=1, sticky='ew', pady=(0,10))
        infoLabel.grid(row=2, column=1, sticky='ew', pady=(0,10))

        bookButton.grid(row=3, column=1, sticky='ew', pady=(0,5))

    #root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.title('')
    root.resizable(width=FALSE, height=FALSE)

    # main screen content
    contentFrame = Frame(root)
    methodFrame = Frame(root)
    routeFrame = Frame(root)

    # config
    for i in range(4):
        methodFrame.grid_columnconfigure(i+1, weight=1)

    # main screen layout
    methodFrame.grid(row=0, column=0, columnspan=2, sticky='ew')
    routeFrame.grid(row=1, column=0, sticky='nw')    
    contentFrame.grid(row=1, column=1, sticky='nsew')

    # travel method frame content
    travelByLabel = Label(methodFrame, text='Travel by:')
    busButton = Button(methodFrame, text='Bus', command=lambda:displayAvailibleRoutes('Bus'))
    trainButton = Button(methodFrame, text='Train', command=lambda:displayAvailibleRoutes('Train'))
    airplaneButton = Button(methodFrame, text='Airplane', command=lambda:displayAvailibleRoutes('Airplane'))
    boatButton = Button(methodFrame, text='Boat', command=lambda:displayAvailibleRoutes('Boat'))

    # travel method layout
    travelByLabel.grid(row=0, column=0, sticky='ew')
    busButton.grid(row=0, column=1, sticky='ew')
    trainButton.grid(row=0, column=2, sticky='ew')
    airplaneButton.grid(row=0, column=3, sticky='ew')
    boatButton.grid(row=0, column=4, sticky='ew') 

signInScreen()
root.withdraw()
updater()

root.mainloop()