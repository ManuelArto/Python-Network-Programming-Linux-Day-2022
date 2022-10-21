from help import *
import socket

# COSTANTI
IP = ''
PORT = 8001
ADDR = (IP, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"


def send(receiver, msg):
	data = {"sender": username, "receiver": receiver, "msg": msg}
	client.send(encode_data(data))

def listen_client():
	while True:
		msg = input("Message: ")

		if msg == DISCONNECT_MESSAGE:
			send("", msg)
			client.close()
			break

		print(f"\n[ACTIVE USERS] {active_users + ['broadcast']}")
		receiver = input("Receiver: ")
		
		if receiver not in active_users + ["broadcast"]:
			print("not a valid username")
			continue

		send(receiver, msg)

def update_users(users):
	global active_users
	users.remove(username)
	active_users = users

def send_username():
	data = {"username": username}
	client.send(encode_data(data))

def listen_server():
	send_username()
	while True:
		data = client.recv(1024)
		data = decode_data(data)
		if not data:
			break
		if "users" in data:
			update_users(data["users"])
		else:
			print(f"\n[NEW MESSAGE] {data['sender']}: {data['msg']}")
			print("Message: ")


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
	print(e)
# finally:
# 	client.close()