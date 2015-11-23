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

random.seed()
prob=1

for rd in range(0,100):
	if random.random() < 0.5:
		s.send('pi\n')
		data=s.recv(SIZE)
		if (not verifyPi(data)):
			print 'Reject'
			break
		else:
			prob=prob*0.5
	else:
		s.send('alpha\n')
		data=s.recv(SIZE)
		if (not verifyAlpha(data)):
			print 'Reject'
			break
		else:
			prob=prob*0.5

print 'Accept'
print 1-prob

s.close()