import socket
import sys
import time

def verifyPi(data):



def veriftAlpha(data):


def verifyCommitment(m,n):
	hashphase='Matrix commitment'
	dimension=len(m)
	for i in range(dimension):
		for j in range(dimension):
			if n[i][j]!=hashlib.sha224(hashphase+str(i)+str(j)+str(m[i][j])).hexdigest()[0]:
				return False
	return True

def parseMatrix(data):
	for c in data:
		if c=='\n':
			break
		dimension=dimension+1
	dimension=dimension/2
	
	m=[[0 for x in range(dimension)] for x in range(dimension)]

	for row,line in enumerate(data.split('\n')):
		for col,val in enumerate(line.split(' ')):
			m[row][col]=int(val)

	return m

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