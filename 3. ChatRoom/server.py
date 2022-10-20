from help import handle_request, active_connections
import json
import socket

# COSTANTI
IP = ''
PORT = 8000
ADDR = (IP, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
# GLOBAL
global active_users

def send_list_active_users():
	users = {"users": list(active_users.keys())}
	for user, client in active_users.items():
		client.send(json.dumps(users).encode())

def send_message(receiver, msg, sender):
	data = {"sender": sender, "msg": msg}
	if receiver.upper() == "BROADCAST":
		for client in active_users:
			client.send(json.dumps(data).encode())
	else:
		client = active_users[receiver]
		client.send(json.dumps(data).encode())

def disconnect_client(username, client):
	print(f"[DISCONNECTING] {username}")
	client.send("DISCONNECTING".encode())
	client.close()
	del active_users[username]
	send_list_active_users()

def read_username(client):
	data = client.recv(1024).decode()
	print(data)
	data = json.loads(data)
	active_users[data["username"]] = client
	send_list_active_users()
	return data["username"]

def listen_client(client, addr):
	username = read_username(client)
	while True:
		msg = client.recv(1024).decode()
		data = json.loads(msg)
		if data["msg"] == DISCONNECT_MESSAGE:
			disconnect_client(username, client)
		else:
			print(f"[MESSAGE] {data}")
			send_message(data["receiver"], data["msg"], data["sender"])


# {username : conn}
active_users = {}
try:
	server = socket.socket()
	server.bind(ADDR)
	server.listen()
	print("[STARTING] server is starting...")
	while True:
		client, addr = server.accept()
		handle_request(listen_client, (client, addr))
		
		# time.sleep(1)

		print(f"[ACTIVE CONNECTIONS] {active_connections()}")
		print(f"[USERS] {list(active_users.keys())}")
except Exception as e:
	# print(e)
	server.close()