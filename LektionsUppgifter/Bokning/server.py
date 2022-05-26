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

def addRoute(instructions):
    sql = "INSERT INTO routes (Origin, Destination, Method, Distance, Price) VALUES (%s, %s, %s, %s, %s);"
    val = (instructions[1], instructions[2], instructions[3], instructions[4], instructions[5])
    mycursor.execute(sql, val)
    
def addUser(instructions):
    print(instructions)
    sql = "INSERT INTO users (firstname, lastname, email, username, password) VALUES (%s, %s, %s, %s, %s);"
    val = (instructions[1], instructions[2], instructions[3], instructions[4], instructions[5])
    mycursor.execute(sql, val)
    mydb.commit()

def editItem(instructions):
    table = instructions[1]
    set_column = instructions[2][0]
    set_value = instructions[2][1]
    where_column = instructions[3][0]
    where_value = instructions[3][1]

    sql = f"UPDATE {table} SET {set_column} = '{set_value}' WHERE {where_column} = '{where_value}'"
    mycursor.execute(sql)

def deleteItem(instructions):
    table = instructions[1]
    where_column = instructions[2][0]
    where_value = instructions[2][1]

    sql = f"DELETE FROM {table} WHERE {where_column} = '{where_value}';"
    mycursor.execute(sql)

def fetchItemData(instructions):
    table = instructions[1]
    select_column = instructions[2]
    where_column = instructions[3][0]
    where_value = instructions[3][1]

    sql = f"SELECT {select_column} FROM {table} WHERE {where_column} = '{where_value}';"
    mycursor.execute(sql)
    answer = mycursor.fetchall()[0][0]
    return answer
    
actionsDic = {
    1:addRoute,
    2:addUser,
    3:editItem,
    4:deleteItem,
    5:fetchItemData
}

def clientHandler(conn):
    instructions = conn.recv(1024).decode('utf-8')
    print('received')
    print(instructions)
    print(type(instructions))
    instructions = eval(instructions)
    print(instructions)
    print(type(instructions))
    userInfo = actionsDic[instructions[0]](instructions)
    print(userInfo)
    if userInfo != '':
        userInfo = userInfo.encode('utf-8')
        conn.send(userInfo)


while True:
    conn, address = s.accept()
    start_new_thread(clientHandler, (conn, ))
    print('new user')

input = input("input:")