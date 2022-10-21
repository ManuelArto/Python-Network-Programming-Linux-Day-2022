from help import *
import socket
import traceback
import time

# COSTANTI
IP = ''
PORT = 8001
ADDR = (IP, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"


def send_message(receiver, msg, sender):
	data = {"sender": sender, "msg": msg}
	if receiver == "broadcast":
		for user, client in active_users.items():
			if user != sender:
				client.send(encode_data(data))
	else:
		client = active_users[receiver]
		client.send(encode_data(data))

def send_list_active_users():
	users = {"users": list(active_users)}
	for user, client in active_users.items():
		client.send(encode_data(users))

def read_username(client):
	data = client.recv(1024)
	data = decode_data(data)
	active_users[data["username"]] = client
	send_list_active_users()
	return data["username"]

def disconnect_client(username):
	print(f"[DISCONNECTING] {username}")
	del active_users[username]
	send_list_active_users()

def listen_client(client, addr, username):
	user = username
	while True:
		data = client.recv(1024)
		data = decode_data(data)
		# data == None se il client si disconnette in modo anomalo
		if not data or data["msg"] == DISCONNECT_MESSAGE:
			disconnect_client(user)
			break
		else:
			print(f"[MESSAGE] {data}")
			send_message(data["receiver"], data["msg"], data["sender"])


# {username1 : conn1, username2 : conn2}
active_users = {}
try:
	server = socket.socket()
	server.bind(ADDR)
	server.listen()
	print("[STARTING] server is starting...")
	while True:
		client, addr = server.accept()
		username = read_username(client)
		handle_request(listen_client, (client, addr, username))
		print(f"[ACTIVE CONNECTIONS] {active_connections()}")
		print(f"[USERS] {list(active_users.keys())}")
except Exception as e:
	print(e)
	traceback.print_exc()
finally:
	server.close()