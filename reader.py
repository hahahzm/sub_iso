import sys
import hashlib

def openMatrix(file):
	with open(file,"r") as mat:
		data=mat.read()
		dimension=1
		for c in data:
			if c=='\n':
				break
			dimension=dimension+1
		dimension=dimension/2
		print dimension
		m=[[0 for x in range(dimension)] for x in range(dimension)]

		for row,line in enumerate(data.split('\n')):
			for col,val in enumerate(line.split(' ')):
				print row, col, val
				if row < dimension and col < dimension:
					m[row][col]=int(val)

		return m

def permute(m, order, size):
	dimension=size
	n1=[[2 for x in range(dimension)] for x in range(dimension)]
	n2=[[2 for x in range(dimension)] for x in range(dimension)]
	
	i=0
	for j in order:
		t=0
		for k in order:
			n1[j][k]=m[i][t]
			t=t+1
		i=i+1

	print 'Half Permuted matrix:'
	for a in n1:
		print a


	i=0
	for j in order:
		t=0
		for k in range(dimension):
			n2[k][j]=n1[k][i]
			t=t+1
		i=i+1

	return n2
	
def commitMatrix(m):
	hashphase='Matrix commitment'
	dimension=len(m)
	n=[[0 for x in range(dimension)] for x in range(dimension)]
	for i in range(dimension):
		for j in range(dimension):
			n[i][j]=hashlib.sha224(hashphase+str(i)+str(j)+str(m[i][j])).hexdigest()[0]
	return n






m=openMatrix(sys.argv[1])

print 'original:'
for a in m:
	print a

order=[2,1,0,3,5,4,7,9,6,8]


n=permute(m, order, len(order))

print 'Permuted matrix:'
for a in n:
	print a

print 'Commitment'

n=commitMatrix(m)
for a in n:
	print a
