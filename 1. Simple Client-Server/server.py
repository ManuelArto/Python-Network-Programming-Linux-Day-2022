import socket

# COSTANTI
IP = ''
PORT = 8000
ADDR = (IP, PORT)

# CREAZIONE del socket server
server = socket.socket()

# BIND dell' address
server.bind(ADDR)
print(f"[START] Socket binded to {PORT}")

# LISTENING
server.listen()

while True:
	# WAITING for clients
	client, addr = server.accept()
	print(f'[NEW CLIENT] ip: {addr}')

	# READ message from client
	msg = client.recv(1024)
	print(f"[NEW MESSAGE from {addr[0]}] {msg.decode()}")

	# WRITE message to client
	client.send(b'Grazie per esserti connesso!')

	# CHIUDI la connessione
	client.close()