from socket import *
def connect_to_server():
    s = socket()                # Skapa ett socket-objekt
    # Ange IP-adress manuellt
    host = "10.32.47.8"
    # t.ex. "localhost" om servern körs på samma dator som klienten
    port = 12345                # Servern körs på port 12345
    s.connect((host, port))     # Anslut till servern
    return s
s = connect_to_server()
b = s.recv(1024)            # Ta emot ett meddelande från servern
msg = b.decode("utf-16")    # Gör om meddelandet från bytekod till vanlig text
msg = input("Skriv något till servern: ")
c = msg.encode("utf-16")
s.send(c)
s.close()
print(msg)
