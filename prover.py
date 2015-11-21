import socket
import sys
from thread import *


def threadServer(socket):
	SIZE=1024
	socket.send('This is Peggy the honest\n')
	default=True
	xlarge=0
	firstTime=True
	passphase='This is Victor'+chr(13)+chr(10)
	while True:
		if default:
			data=socket.recv(SIZE)
		else:
			data=socket.recv(xlarge)

		if not data:
			break

		if firstTime and not(str(data) == passphase):
			print data + 'is Invalid Request'
			for c in data:
				print ord(c)
			print '******************'
			for c in passphase:
				print ord(c)
			break




		reply='Oh s..' + data
		socket.sendall(reply)
		print data,
		firstTime=False
	socket.close()


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