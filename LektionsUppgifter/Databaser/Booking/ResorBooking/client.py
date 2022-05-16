from tkinter import *
import mysql.connector


mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='Prog2'
)
mycursor = mydb.cursor()

class Route:
    def __init__(self, start, destination):
        self.start = start
        self.destination = destination


root = Tk()

w = root.winfo_screenwidth()
h = root.winfo_screenheight()

def showRoute(Route):

    pass

def register():
    pass
def login():
    pass

def registerScreen():
    register_screen = Toplevel()
    register_screen.grid_rowconfigure(0, weight=1)
    register_screen.grid_columnconfigure(0, weight=1)

    FirstName = Label(register_screen, text='First name:')
    LastName= Label(register_screen, text='Surname:')
    username = Label(register_screen, text='Username:')
    Password = Label(register_screen, text='Password:')
    Register = Label(register_screen)
    Login = Label(register_screen, text='Already a member?')

    FirstNameEntry = Entry(register_screen)
    LastNameEntry = Entry(register_screen)
    UsernameEntry = Entry(register_screen)
    PasswordEntry = Entry(register_screen, show='*')

    RegisterButton = Button(register_screen,text='Register', command=register)
    LoginButton = Button(register_screen, text='Login here!', command=loginScreen)
    
def loginScreen():
    login_screen = Toplevel()
    login_screen.grid_rowconfigure(0, weight=1)
    login_screen.grid_columnconfigure(0, weight=1)

    usernameLabel = Label(login_screen, text='Username:')
    passwordLabel = Label(login_screen, text='Password:')       
    registerLabel = Label(login_screen, text='Not a member?')

    usernameEntry = Entry(login_screen)
    passwordEntry = Entry(login_screen, show='*')

    showPasswordButton = Button(login_screen, text='S')
    loginButton = Button(login_screen, text='Login', command=login)
    registerButton = Button(login_screen, text='Register here!', command=registerScreen)

    # login screen layout
    usernameLabel.grid(row=0, column=0, columnspan=4, sticky='ew', pady=(5,0))
    usernameEntry.grid(row=1, column=0, columnspan=4, sticky='ew', padx=5, pady=(0,5))

    passwordLabel.grid(row=2, column=0, columnspan=4, sticky='ew')
    passwordEntry.grid(row=3, column=0, columnspan=3, sticky='ew', padx=(5,0), pady=(0,20))
    showPasswordButton.grid(row=3, column=3, sticky='ew', padx=(0,5), pady=(0,20))

    loginButton.grid(row=5, column=0, columnspan=4, sticky='ew', padx=5, pady=(0,40))

    registerLabel.grid(row=7, column=1, sticky='e', pady=(0,5))
    registerButton.grid(row=7, column=2, columnspan=2, sticky='w', padx=(0,5), pady=(0,5))

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
    busButton = Button(methodFrame, text='Bus', command=lambda:selected_method='bus')
    trainButton = Button(methodFrame, text='Train', command=lambda:selected_method='train')
    airplaneButton = Button(methodFrame, text='Airplane', command=lambda:selected_method='airplane')
    boatButton = Button(methodFrame, text='Boat', command=lambda:selected_method='boat')

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
            

loginScreen()

root.mainloop()