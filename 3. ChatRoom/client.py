from help import handle_request
import socket
import json

# COSTANTI
IP = ''
PORT = 8000
ADDR = (IP, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
# GLOBAL
global active_users

def send(self, receiver, msg):
	data = {"sender": username, "receiver": receiver, "msg": msg}
	client.send(json.dumps(data).encode())

def listen_client():
	while True:
		msg = input("Message: ")

		if msg == DISCONNECT_MESSAGE:
			send("", DISCONNECT_MESSAGE.encode())
			break

		print(f"\n[ACTIVE USERS] {active_users + ['broadcast']}")
		receiver = input("Receiver: ")
		
		if receiver not in list(active_users.keys()) + ["broadcast"]:
			print("not a valid username")
			continue

		send(receiver, msg.encode())

def update_users(users):
	del users[username]
	active_users = users

def send_username():
	data = {"username": username}
	client.send(json.dumps(data).encode())

def listen_server():
	send_username()
	while True:
		data = client.recv(1024).decode()
		data = json.loads(data)
		if "users" in data.keys():
			update_users(data["users"])
		else:
			print(f"\n[NEW MESSAGE] {data['sender']}: {msg} \nMessage: ", end="")


# [user1, user2]
active_users = []

try:
	username = input("Insert username: ")
	client = socket.socket()
	client.connect(ADDR)
	print(f"[CONNECTION] Starting connection to {ADDR}")
	
	handle_request(target=listen_server)
	listen_client()

except Exception as e:
	# print(e)
	client.close()
