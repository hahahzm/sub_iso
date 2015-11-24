import socket
import sys
import random
import hashlib
from thread import *

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

def matToStr(m):
	dimension=len(m)
	result=''
	for i in range(dimension):
		for j in range(dimension):
			result=result+str(m[i][j])
			if j != dimension-1:	
				result=result+' '
		if i != dimension-1:
			result=result+'\n'
	return result

def listToStr(l):
	dimension=len(l)
	result=''
	for i in range(dimension):
		result=result+str(l[i])
		if i != dimension-1:	
			result=result+' '

	return result

def commitMatrix(m):
	hashphase='Matrix commitment'
	dimension=len(m)
	n=[[0 for x in range(dimension)] for x in range(dimension)]
	for i in range(dimension):
		for j in range(dimension):
			n[i][j]=str(int(hashlib.sha224(hashphase+str(i)+str(j)+str(m[i][j])).hexdigest(),16))[0]
	return n

def generateAlpha(size):
	result = []
	for x in range(0,size):
		result.append(x)
	random.shuffle(result)
	return result

def generatePi(alpha):
	m=[]
	ct=0
	global path
	secret=path+"G1-G'"
	with open(secret,"r") as order:
		
		for data in order:
			n=[0 for x in range(2)]
			for col,val in enumerate(data.split(' ')):
				n[col]=int(val)
			m.append(n)
			ct=ct+1

	n=[0 for x in range(ct)]

	for line in m:
		n[line[0]]=alpha[line[1]]

	return n
		
def permutation(size):
	result=[]
	for x in range(size):
		result.append(x)
	random.seed()
	random.shuffle(result)
	return result

#def permute(m, order, size):
#	dimension=size
#	n1=[[2 for x in range(dimension)] for x in range(dimension)]
#	n2=[[2 for x in range(dimension)] for x in range(dimension)]
#	
#	i=0
#	for j in order:
#		for k in range(dimension):
#			n1[j][k]=m[i][k]
#		i=i+1
#
#	i=0
#	for j in order:
#		for k in range(dimension):
#			n2[k][j]=n1[k][i]
#		i=i+1

#	return n2

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

def threadServer(socket):
	SIZE=1024
	socket.send('This is Peggy the honest\n')
	default=True
	xlarge=0
	firstTime=True
	passphase='This is Victor'+chr(13)+chr(10)
	global g1
	global g2
	
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
			order=permutation(len(g2))
			q=permute(g2, order, len(g2))
			orderPi=generatePi(order)
			q_prime=permute(g1, orderPi, len(g2))


			if str(data) == 'commitment'+chr(13)+chr(10):
				socket.sendall(matToStr(commitMatrix(q)))
				data=socket.recv(SIZE)

			if str(data) == 'alpha'+chr(13)+chr(10):
				print('Providing alpha and the adj matrix Q\n')
				socket.sendall(listToStr(order))
				data=socket.recv(SIZE)
				socket.sendall(matToStr(q))
			elif str(data) == 'pi'+chr(13)+chr(10):
				print 'Providing pi and portion of the adj matrix of Q'
				socket.sendall(listToStr(orderPi))
				data=socket.recv(SIZE)
				socket.sendall(matToStr(q_prime))

			else:
				socket.sendall('You know you should have trusted in me\n')
				print 'Now he is convinced\n'
				break
		firstTime=False

	socket.close()


HOST = ''
PORT = int(sys.argv[1])

path = sys.argv[2]
g1=openMatrix("G1")
g2=openMatrix("G2")



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