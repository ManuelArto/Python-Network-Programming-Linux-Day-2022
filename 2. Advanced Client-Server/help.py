import threading

def handle_wrapper(target, address):
	try:
		target(*address)
	except Exception as e:
		print("[ERROR] Client forced disconnection")
		address[0].close()

def handle_request(target, address):
	thread = threading.Thread(target=handle_wrapper, args=(target, address))
	thread.start()