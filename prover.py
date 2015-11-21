import socket
import sys
from thread import *


def threadServer(socket):
	SIZE=1024
	conn.send('O ha yo u ~\n')
	while True:
		data=conn.recv(SIZE)
		reply='WTF...' + data
		if not data:
			break
		conn.sendall(reply)
		print data
	conn.close()


HOST = ''
PORT = int(sys.argv[1])

# create socket
s = socket.socket(
	socket.AF_INET, socket.SOCK_STREAM)

print s

# bind socket 
try:
	s.bind((HOST, PORT))
except socket.error as errmsg:
	print 'Binding error:' + str(errmsg[0]) + ':' + errmsg[1]
	sys.exit()

# listen to socket
s.listen(10)

#talking to client
while True:
	conn, addr = s.accept()
	print 'Connected with' + addr[0] + ':' + str(addr[1])

	start_new_thread(threadServer, (conn,))

s.close()