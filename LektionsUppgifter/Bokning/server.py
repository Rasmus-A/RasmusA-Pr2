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
    origin = instructions[1]
    destination = instructions[2]
    method = instructions[3]
    distance = int(instructions[4])
    price = int(instructions[5])
    sql = "INSERT INTO routes (Origin, Destination, Method, Distance, Price) VALUES (%s, %s, %s, %s, %s);"
    val = (origin, destination, method, distance, price)
    mycursor.execute(sql, val)
    mydb.commit()
    
def addUser(instructions):
    print(instructions)
    sql = "INSERT INTO users (firstname, lastname, email, username, password) VALUES (%s, %s, %s, %s, %s);"
    val = (instructions[1], instructions[2], instructions[3], instructions[4], instructions[5])
    mycursor.execute(sql, val)
    mydb.commit()

def updateRoute(instructions):
    origin = instructions[1]
    destination = instructions[2]
    method = instructions[3]
    distance = int(instructions[4])
    price = int(instructions[5])
    id = int(instructions[6])
    print(instructions)
    sql = f"UPDATE routes SET Origin = '{origin}', Destination = '{destination}', Method = '{method}', Distance = {distance}, Price = {price} WHERE id = {id};"
    print(sql)
    mycursor.execute(sql)
    mydb.commit()

def deleteItem(instructions):
    table = instructions[1]
    where_column = instructions[2]
    where_value = instructions[3]

    sql = f"DELETE FROM {table} WHERE {where_column} = '{where_value}';"
    print(sql)
    mycursor.execute(sql)
    mydb.commit()

def fetchItemData(instructions):
    print(instructions)
    print(len(instructions))
    select_column = instructions[1]
    table = instructions[2]

    if len(instructions) == 3:
        sql = f"SELECT {select_column} FROM {table};"

    elif len(instructions) == 5:
        where_column = instructions[3]
        where_value = instructions[4]

        sql = f"SELECT {select_column} FROM {table} WHERE {where_column} = '{where_value}';"

    mycursor.execute(sql)
    answer = mycursor.fetchall()
    for i in range(len(answer)):
        answer[i] = answer[i][0]
    return answer

actionsDic = {
    1:addRoute,
    2:addUser,
    3:updateRoute,
    4:deleteItem,
    5:fetchItemData,
}

def clientHandler(conn):
    while True:
        instructions = conn.recv(1024).decode('utf-8')
        print('received')
        print(instructions)
        print(type(instructions))
        instructions = instructions.split(",")
        instructions[0] = int(instructions[0])
        print(instructions)
        print(type(instructions))
        userInfo = actionsDic[instructions[0]](instructions)
        print(userInfo)
        if userInfo != None:
            userInfo = ",".join(map(str, userInfo)).encode('utf-8')
            conn.send(userInfo)


while True:
    conn, address = s.accept()
    start_new_thread(clientHandler, (conn, ))
    print('new user')

input = input("input:")