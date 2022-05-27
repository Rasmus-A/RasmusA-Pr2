from tkinter import *
import hashlib
from pyparsing import col
from socket import *
from _thread import *


selected_method=''
passwordVisibility = ('S')



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
        print('i live')
    
    def getRoute(self):
        self._origin = fetchItemInfo('origin', 'routes', 'id', self._id)[0]
        self._destination = fetchItemInfo('destination', 'routes', 'id', self._id)[0]
        self._method = fetchItemInfo('method', 'routes', 'id', self._id)[0]
        self._distance = int(fetchItemInfo('distance', 'routes', 'id', self._id)[0])
        self._price = int(fetchItemInfo('price', 'routes', 'id', self._id)[0])

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
        self.time = self._distance/80

class TrainRoute(RouteOnSurface):
    def __init__(self, id):
        super().__init__(id)
        self.time = self._distance/200

class BoatRoute(RouteOnSurface):
    def __init__(self, id):
        super().__init__(id)
        self.time = self._distance/45

class AirplaneRoute(RouteInAir):
    def __init__(self, id):
        super().__init__(id)
        self.time = self._distance/900



root = Tk()

w = root.winfo_screenwidth()
h = root.winfo_screenheight()

def showRoute(Route):

    pass

def selectMethod(method):
    selected_method=method



def fetchItemInfo(*request):   # info tuple på formen SELECT (sökt information) FROM (table) WHERE (kolumnnamn) = (värde)
    answer = []
    for i in request:
        print(i)
        instructions = ",".join([5, i.split(",")])
        print(instructions)
        instructions = instructions.encode('utf-8')
        conn.send(instructions)
        data = conn.recv(1024).decode('utf-8')
        answer.append(eval(data))
    return answer

def register(firstName, lastName, email, username, password):
    global registerErrorLabel
    hashedPassword = hashlib.sha256(password.encode('utf-8'))
    print(hashedPassword.digest())
    instructions = str([3, firstName, lastName, email, username, hashedPassword.hexdigest()]).encode('utf-8')
    try:
        conn.send(instructions)
        root.deiconify()
    except:
        registerErrorLabel.config(text='Registration failed, please try again')
    
    
def signIn(username, password):
    global signInErrorLabel        
    hashedPassword = hashlib.sha256(password.encode('utf-8'))
    data = fetchItemInfo(('password','users', 'username', username))
    password = data[0][0]
    try:
        print('Waiting for response')
        if hashedPassword.hexdigest() == password[0]:
            signIn_screen.withdraw()
            root.deiconify()
        elif hashedPassword.hexdigest() != password[0]:
            signInErrorLabel.configure(text='Incorrect username or password')
    except:
        print('error')
        signInErrorLabel.configure(text='An error has occured, please try again')
        

def registerScreen():
    global registerErrorLabel, register_screen
    def passwordConfig():
        if passwordVisibility.get() == 'S':
            pass
    # Register screen content
    register_screen = Toplevel()
    register_screen.title('Register')
    register_screen.geometry('250x415')
    register_screen.resizable(height = False, width = False)
    register_screen.grid_rowconfigure(0, weight=1)
    register_screen.grid_columnconfigure(0, weight=1)

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

    showPasswordButton = Button(register_screen, textvariable=passwordVisibility)
    registerButton = Button(register_screen,text='Register', command=lambda: [register(firstNameEntry.get(), lastNameEntry.get(), emailEntry.get(), usernameEntry.get(), passwordEntry.get()), register_screen.withdraw()])
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
    global signInErrorLabel, signIn_screen
    # Sign in screen content
    signIn_screen = Toplevel()
    signIn_screen.title('Sign In')
    signIn_screen.geometry('250x260')
    signIn_screen.resizable(height = False, width = False)
    signIn_screen.grid_rowconfigure(0, weight=1)
    signIn_screen.grid_columnconfigure(0, weight=1)

    usernameLabel = Label(signIn_screen, text='Username:')
    passwordLabel = Label(signIn_screen, text='Password:')
    signInErrorLabel = Label(signIn_screen, text=' ')       
    registerLabel = Label(signIn_screen, text='Not a member?')

    usernameEntry = Entry(signIn_screen)
    passwordEntry = Entry(signIn_screen, show='*')

    showPasswordButton = Button(signIn_screen, text='S')
    signInButton = Button(signIn_screen, text='Login', command=lambda: [signIn(usernameEntry.get(), passwordEntry.get())])
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

def mainScreen():
    main_screen = Toplevel()
    main_screen.grid_rowconfigure(0, weight=1)
    main_screen.grid_columnconfigure(0, weight=1)
    main_screen.title('Insert name here')

    # main screen content
    contentFrame = Frame(main_screen)
    methodFrame = Frame(main_screen)
    routeFrame = Frame(main_screen)

    # main screen layout
    methodFrame.grid(row=0, column=0, columnspan=2, sticky='ew')
    routeFrame.grid(row=1, column=0, sticky='ns')    
    contentFrame.grid(row=1, column=1, sticky='nsew')

    # content frame content
    startLabel = Label(contentFrame, text='')
    destinationLabel = Label(contentFrame, text='')

    # travel method frame content
    travelByLabel = Label(methodFrame, text='Travel by:')
    busButton = Button(methodFrame, text='Bus', command=lambda:selectMethod('Bus'))
    trainButton = Button(methodFrame, text='Train', command=lambda:selectMethod('Train'))
    airplaneButton = Button(methodFrame, text='Airplane', command=lambda:selectMethod('Airplane'))
    boatButton = Button(methodFrame, text='Boat', command=lambda:selectMethod('Boat'))

    # travel method layout
    travelByLabel.grid(column=0, sticky='ew')
    busButton.grid(column=1, sticky='ew')
    trainButton.grid(column=2, sticky='ew')
    airplaneButton.grid(column=3, sticky='ew')
    boatButton.grid(column=4, sticky='ew') 

    # route screen content
    for i in Route:
        if Route.method == selected_method:
            Route.name = Button(routeFrame, textvariable=Route.name, command=lambda:showRoute(Route))

signInScreen()
root.withdraw()

root.mainloop()