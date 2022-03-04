from socket import *
from _thread import *

def start_server():         # Samma som i förra exemplet
    s = socket()
    host = "localhost"
    port = 12345
    s.bind((host, port))
    s.listen()
    return s
def threaded_client(connection):    # Definierar vad tråden ska göra
    msg = "Servern säger hej till klienten!"
    connection.send(msg.encode("utf-16"))
    while True:
        data = connection.recv(1024)
        msg = "Servern tog emot följande meddelande: " \
              + data.decode("utf-16")
        print(msg)
        connection.send(msg.encode("utf-16"))
def threaded_server():
    


start_new_thread(threaded_server)

s = start_server()
ThreadCount = 0
while True: # Skapar en ny tråd för varje klient som ansluter
    print("Väntar på att en klient ska ansluta till servern...")
    conn, address = s.accept()
    print("En ny klient anslöt: " + address[0] + ':'
          + str(address[1]))
    start_new_thread(threaded_client, (conn, ))
    ThreadCount += 1
    print("Tråd nummer: " + str(ThreadCount))