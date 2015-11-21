import socket
import sys
import time

HOST = str(sys.argv[1])
PORT = int(sys.argv[2])
SIZE = 1024

passphase='Chanllenge me\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to host
s.connect((HOST, PORT))
data=s.recv(SIZE)

s.send('This is Victor'+chr(13)+chr(10))

data=s.recv(SIZE)
print data


s.close()