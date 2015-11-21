import socket
import sys
import time

HOST = str(sys.argv[1])
PORT = int(sys.argv[2])
SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to host
s.connect((HOST, PORT))

s.send('first second last \n\n\n\n')

data=s.recv(SIZE)
print data

s.close()