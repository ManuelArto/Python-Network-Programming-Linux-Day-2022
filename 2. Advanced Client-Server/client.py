import socket
 
# COSTANTI
IP = ''
PORT = 8000
ADDR = (IP, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

# CREAZIONE del socket client
client = socket.socket()

# CONNESSIONE al server
client.connect(ADDR)

msg = ""
while msg != DISCONNECT_MESSAGE:
    # WRITE message to server
    msg = input("Send: ")
    client.send(msg.encode())

    # READ message from server
    receive = client.recv(1024)
    print(receive.decode())

# CHIUDI la connessione
client.close()