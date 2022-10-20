import threading
import json

def handle_wrapper(target, address):
	# try:
	target(*address)
	# except Exception as e:
	# 	print(e)
	# 	address[0].close()

def handle_request(target, address):
	thread = threading.Thread(target=handle_wrapper, args=(target, address))
	thread.start()

def active_connections():
	return threading.activeCount() - 1
