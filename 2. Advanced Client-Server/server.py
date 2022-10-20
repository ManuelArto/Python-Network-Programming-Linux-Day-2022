from help import handle_request
import socket

# COSTANTI
IP = ''
PORT = 8000
ADDR = (IP, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

def handle_client(client, addr):
	print(f'[NEW CLIENT] ip: {addr}')
	msg = ""
	while msg != DISCONNECT_MESSAGE:
		# READ message from client
		msg = client.recv(1024).decode()
		print(f"[NEW MESSAGE from {addr[0]}] {msg}")

		# WRITE message to client
		client.send(f'Message received from {addr[0]}'.encode())

	# CHIUDI la connessione
	client.close()


# CREAZIONE del socket server
server = socket.socket()

# BIND dell' address
server.bind(ADDR)
print(f"[START] Socket binded to {PORT}")

# LISTENING
server.listen()

try:
	while True:
		# WAITING for clients
		client, addr = server.accept()
		handle_request(handle_client, (client, addr))
except KeyboardInterrupt as e:
	server.close()