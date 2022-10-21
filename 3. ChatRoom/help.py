import threading
import traceback
import json

# Threading helper

def handle_wrapper(target, args):
	try:
		target(*args)
	except Exception as e:
		pass
		# print(e)
		# traceback.print_exc()

def handle_request(target, args = []):
	thread = threading.Thread(target=handle_wrapper, args=(target, args))
	thread.start()

def active_connections():
	return threading.activeCount() - 1

# Json helper

def encode_data(data):
	return json.dumps(data).encode()

def decode_data(data):
	return json.loads(data.decode()) if data else None