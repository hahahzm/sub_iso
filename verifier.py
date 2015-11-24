import socket
import sys
import time
import random

path="graphs/"

def openMatrix(file):
	global path
	with open(path + file,"r") as mat:
		data=mat.read()
		dimension=1
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

def permute(m, order, size):
	dimension=size
	n=[[2 for x in range(dimension)] for x in range(dimension)]
	
	i=0
	for j in order:
		t=0
		for k in order:
			n[j][k]=m[i][t]
			t=t+1
		i=i+1

	return n




def matIsEqual(m,n):
	dimension=len(m)
	for i in range(dimension):
		for j in range(dimension):
			if m[i][j]!=n[i][j]:
				return False
	return True





def verifyAlpha(g2, q, order):
	realg2=permute(g2, order, len(g2))
	if not matIsEqual(q, realg2):
		return False
	return True


def verifyPi(g1, q_prime, orderPi):
	real_q_prime=permute(g1, orderPi, len(q_prime))
	if not matIsEqual(real_q_prime, q_prime):
		return False
	return True


def verifyCommitment(m,n):
	hashphase='Matrix commitment'
	dimension=len(m)
	for i in range(dimension):
		for j in range(dimension):
			if m[i][j]!=2:
				if n[i][j]!=str(int(hashlib.sha224(hashphase+str(i)+str(j)+str(m[i][j])).hexdigest(),16))[0]:
					return False
	return True

def parseMatrix(data):
	dimension=1
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

def parseList(data):
	m=[]
	for col,val in enumerate(data.split(' ')):
		m.append(int(val))
	return m

HOST = str(sys.argv[1])
PORT = int(sys.argv[2])
SIZE = 1024

path = sys.argv[3]

g1=openMatrix("G1")
g2=openMatrix("G2")


passphase='Chanllenge me\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to host
s.connect((HOST, PORT))
data=s.recv(SIZE)

s.send('This is Victor'+chr(13)+chr(10))

data=s.recv(SIZE)
##print data

random.seed()
prob=float(1)

for rd in range(0,100):

	s.send('commitment'+chr(13)+chr(10))

	data=s.recv(SIZE)
	#print "RECEIVED COMMITMENT:"+data
	commitment=parseMatrix(data)

	if random.random() < 0.5:
		s.sendall('pi'+chr(13)+chr(10))
		data=s.recv(SIZE)
		#print "RECEIVED PI:"+data
		orderPi=parseList(data)

		s.sendall('matrix'+chr(13)+chr(10))
		data=s.recv(SIZE)
		q_prime=parseMatrix(data)

		if (not verifyPi(g1, q_prime, orderPi)) and (not verifyCommitment(q_prime, commitment)):
			print 'Reject'
			break
		else:
			print "Round", rd, "case B: passed"
			prob=prob*0.5
	else:
		s.sendall('alpha'+chr(13)+chr(10))
		data=s.recv(SIZE)
		#print "RECEIVED ALPHA:"+data
		order=parseList(data)

		s.sendall('matrix'+chr(13)+chr(10))
		data=s.recv(SIZE)
		q=parseMatrix(data)

		if (not verifyAlpha(g2, q, order)) and (not verifyCommitment(q, commitment)):
			print 'Reject'
			break
		else:
			print "Round", rd, "case A: passed"
			prob=prob*0.5


print "Probility of Peggy knows the subgraph: ", 1-prob
s.send('...')
s.close()