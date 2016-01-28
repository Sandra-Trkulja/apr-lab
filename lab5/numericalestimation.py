import sys
import matplotlib.pyplot as plt
from copy import deepcopy
from Matrix import Matrix


T = 0.1 # default time interval
tmax = 10 # default interval [0, tmax]

def rungekutta(A, x0, B = None, T = T, tmax = tmax, iters = 1):
	B = _checkfixestimationtypes(A, B, x0)
	x = []
	x.append((0, x0))
	count = 0
	for i in drange(0+T, tmax, T):
		count += 1
		m1 = evaldx(A, x[-1][1], B)

		xknew = x[-1][1] + T * m1 * 0.5
		m2 = evaldx(A, xknew, B)

		xknew  = x[-1][1] + T * m2 * 0.5
		m3 = evaldx(A, xknew, B)

		xknew  = x[-1][1] + T * m3
		m4 = evaldx(A, xknew, B)

		x.append((i, x[-1][1] + T * (m1 + 2 * m2 + 2 * m3 + m4) * (1/6)))

		if count % iters == 0:
			print('Iteracija: ' + str(count) + '\nm1: \n' + str(m1) + '\nm2:\n' + str(m2) + '\nm3:\n' + str(m3) + '\nm4:\n' + str(m4) + '\nxnew:\n' + str(x[-1][1]) + '\n')

	drawx(x)

def trapezoidal(A, x0, B = None, T = T, tmax = tmax, iters = 1):
	B = _checkfixestimationtypes(A, B, x0)
	x = []
	x.append((0, x0))
	count = 0
	for i in drange(0+T, tmax, T):
		count += 1
		
		Ahalf = 0.5 * T * A
		I = I = Matrix([[1 if i == j else 0 for j in A.m] for i in A.m])

		sigma = ~(I - Ahalf) * (I + Ahalf)
		Bnew = ~(I - Ahalf) * T * B

		xknew = evaldx(sigma, x[-1][1], Bnew)

		x.append((i, xknew))

		if count % iters == 0:
			print('Iteracija: ' + str(count) + '\nsigma: \n' + str(sigma) + '\nBnew:\n' + str(Bnew) + '\nxknew:\n' + str(xknew) + '\n')

	drawx(x)

def drawx(a):
	t, x, y = getaxiselements(a)
	plt.plot(t, x, 'b')
	plt.plot(t, y, 'r')
	plt.show()

def evaldx(A, x0, B):
	return A * x0 + B

def drange(start, stop, step):
	r = start
	while r < stop:
		yield r
		r += step

def getaxiselements(a):
	t, x, y = [], [], []
	for i in range(len(a)):
		t.append(a[i][0])
		x.append(a[i][1][0, 0])
		y.append(a[i][1][1, 0])
	return t, x, y

def _checkfixestimationtypes(A, B, x0):
	if type(A) != Matrix or (B is not None and type(B) is not Matrix):
		print('Matrices A and B should be of type Matrix.')
		sys.exit(-1)
	if not A.issquarematrix() or A.rows != 2:
		print('Matrix A should be a square 2x2 matrix.')
		sys.exit(-1)
	if type(x0) != Matrix or x0.rows != A.rows or x0.cols != 1:
		print('Matrix x0 should be a column matrix.')
		sys.exit(-1)
	if B is None:
		B = Matrix([[0 for j in range(1)] for i in range(A.rows)])
	return B