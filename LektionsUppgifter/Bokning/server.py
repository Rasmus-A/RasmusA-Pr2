from socket import *
from _thread import *
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='prog2'
)
mycursor = mydb.cursor()

def start_server():
    s = socket()
    host = "localhost"
    port = 12345
    s.bind((host, port))
    s.listen()
    return s
s = start_server()

def addRoute():
    pass

def editRoute():
    pass

def addUser(data):
    print(data)
    sql = "INSERT INTO users (firstname, lastname, email, username, password) VALUES (%s, %s, %s, %s, %s)"
    val = (data[1], data[2], data[3], data[4], data[5])
    mycursor.execute(sql, val)
    mydb.commit()

def editUser():
    pass

actionsDic = {
    1:addRoute,
    2:editRoute,
    3:addUser,
    4:editUser
}

def clientHandler(conn):
    data = conn.recv(1024)
    print('received')
    data = data.decode('utf-8')
    print(data)
    data = eval(data)
    print(data)
    actionsDic[data[0]](data)
    print('success')
while True:
    conn, address = s.accept()
    start_new_thread(clientHandler, (conn, ))
    print('new user')

input = input("input:")