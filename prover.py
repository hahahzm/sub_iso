import socket
import sys
import random
import hashlib
from thread import *

def openMatrix(file):
	with open(file,"r") as mat:
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

def commitMatrix(m):
	hashphase='Matrix commitment'
	dimension=len(m)
	n=[[0 for x in range(dimension)] for x in range(dimension)]
	for i in range(dimension):
		for j in range(dimension):
			n[i][j]=hashlib.sha224(hashphase+str(i)+str(j)+str(m[i][j])).hexdigest()[0]
	return n

def permutationArray(size):
	result = []
	for x in range(0,size):
		result.append(x)
	random.shuffle(result)
	return result


def permute(m, order):
	dimension=len(m)
	n1=[[0 for x in range(dimension)] for x in range(dimension)]
	n2=[[0 for x in range(dimension)] for x in range(dimension)]
	
	i=0
	for j in order:
		for k in range(dimension):
			n1[j][k]=m[i][k]
		i=i+1

	i=0
	for j in order:
		for k in range(dimension):
			n2[k][j]=n1[k][i]
		i=i+1
		
	return n2

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
			default=True

		if not data:
			break

		if firstTime and not(str(data) == passphase):
			print 'Invalid Request'
			break
			
		if firstTime:
			socket.sendall('Chanllenge me\n')
			print 'Bingo'
		else:
			if str(data) == 'pi\n':
				print 'Providing pi and portion of the adj matrix of Q'
				socket.sendall(str(permutation(10)))
			elif str(data) == 'alpha\n':
				socket.sendall('Providing alpha and the adj matrix Q\n')
			else:
				socket.sendall('You know you should have trusted in me\n')
				print 'Now he is convinced\n'
				break
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