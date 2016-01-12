import sys

class Matrix(object):
	
	def __init__(self, matrix):
		self.m = matrix
		self.rows = len(self.m)
		self.cols = len(self.m[0])

	def __getitem__(self, index):
		x, y = index
		self._checkaccess(x, y)
		return self.m[x][y]

	def __setitem__(self, index, item):
		x, y = index
		self._checkaccess(x, y)
		self.m[x][y] = item

	def __add__(self, other):
		self._checkdimensions(other, 'addition')
		result = [[self[i, j] + other[i, j] for j in range(self.cols)] for i in range(self.rows)]
		return Matrix(result)

	def __iadd__(self, other):
		self.printpretty()
		self._checkdimensions(other, 'addition')
		self.m = [[self[i, j] + other[i, j] for j in range(self.cols)] for i in range(self.rows)]
		return self

	def __sub__(self, other):
		self._checkdimensions(other, 'substraction')
		result = [[self[i, j] - other[i, j] for j in range(self.cols)] for i in range(self.rows)]
		return Matrix(result)

	def __isub__(self, other):
		self._checkdimensions(other, 'substraction')
		self.m = [[self[i, j] - other[i, j] for j in range(self.cols)] for i in range(self.rows)]
		return self

	def __mul__(self, other):
		if type(other) in [int, float]:
			result = [[self[i, j] * other for j in range(self.cols)] for i in range(self.rows)]
			return Matrix(result)
		elif type(other) == Matrix:
			if not (self.cols == other.rows):
				print('Cannot continue multiplication. Matrices are not alligned.')
				sys.exit(-1)
			result = [[sum(self[i, k] * other[k, j] for k in range(self.cols)) for j in range(other.cols)] for i in range(self.rows)]
			return Matrix(result)

	def __rmul__(self, other):
		return Matrix.__mul__(self, other)

	def __invert__(self): #used for transposin
		result = [[self[i, j] for i in range(self.rows)] for j in range(self.cols)]
		return Matrix(result)

	def __eq__(self, other):
		eps = 1e-6
		self._checkdimensions(other, 'equality')
		for i in range(self.rows):
			for j in range(self.cols):
				if abs(self[i, j] - other[i, j]) > eps:
					return False
		return True

	def __str__(self, width=35, precision=10):
		return '\n'.join([''.join(['{0:{1}.{2}f}'.format(item, width, precision) for item in row]) for row in self.m])

	@classmethod
	def fromfile(cls, matrix_path):
		matrix = []
		with open(matrix_path, 'r') as f:
			for row in f.readlines():
				matrix.append([float(x) for x in row.split()])
		return Matrix(matrix)

	def _checkdimensions(self, other, operation):
		if not (self.rows == other.rows and self.cols == other.cols):
			print('Cannot continue ' + operation + '. Matrix dimensions don\'t match.')
			sys.exit(-1)
		return

	def _checkaccess(self, x, y):
		if x < 0 or x >= self.rows or y < 0 or y >= self.cols:
			print('Cannot access element ({0},{1}) because it is out of the range ({2},{3}).'.format(x, y, self.rows, self.cols))
			sys.exit(-1)
		return

	def _checksubstitutiondim(self, other, P=None):
		if type(other) != Matrix:
			print('The right side of substitution must be a matrix of class Matrix.')
			sys.exit(-1)
		if self.rows != self.cols or self.rows != other.rows or other.cols != 1:
			print('Substitution equation dimensions must be nxn * nx1 = nx1.')
			sys.exit(-1)
		if type(P) == Matrix:
			if other.rows != P.rows or P.cols != 1:
				print('Substitution cannot continue because permutation matrix dimensions don\'t match.')
				sys.exit(-1)

	def printtofile(self, filename):
		with open(filename, 'w') as f:
			print("\n".join([' '.join([str(x) for x in row]) for row in self.m]), file=f)

	def issquarematrix(self):
		if self.rows == self.cols:
			return True
		return False

	def forwardsubstitution(self, b, P):
		self._checksubstitutiondim(b, P)
		y = ~Matrix([[0] * self.rows])
		for i in range(self.rows):
			y[i, 0] = b[P[i, 0], 0]
			for j in range(i):
				y[i,0] -= self[i, j] * y[j, 0]
		return y

	def backwardsubstitution(self, y):
		self._checksubstitutiondim(y)
		x = ~Matrix([[0] * self.rows])
		for i in reversed(range(self.rows)):
			x[i, 0] = y[i, 0]
			for j in range(i + 1, self.cols):
				x[i,0] -= self[i, j] * x[j, 0]
			x[i, 0] /= self[i, i]
		return x

	def LUdecomposition(self):
		eps = 1e-6
		if not self.issquarematrix():
			print('LU substitution can only be done on square matrices.')
			sys.exit(-1)
		for k in range(self.rows - 1):
			for i in range(k + 1, self.rows):
				if abs(self[k, k]) < eps:
					print('LU substitution has zero on diagonal. Division by zero is not allowed.')
					sys.exit(-1)
				self[i, k] /= self[k, k]
				for j in range(k + 1, self.rows):
					self[i, j] -= self[i, k] * self[k, j]
		P = Matrix([[i] for i in range(self.rows)])
		return self, P

	def LUPdecomposition(self):
		eps = 1e-6
		if not self.issquarematrix():
			print('LUP substitution can only be done on square matrices.')
			sys.exit(-1)
		P = Matrix([[i] for i in range(self.rows)])
		for k in range(self.rows - 1):
			pivot = 0.0
			l = 0
			for i in range(k, self.rows):
				if (abs(self[i, k]) > pivot):
					pivot = abs(self[i, k])
					l = i
			if abs(pivot) < eps:
				print('Matrix is singular. LUP decomposition cannot continue.')
				sys.exit(-1)

			P[k, 0], P[l, 0] = P[l, 0], P[k, 0]
			for j in range(self.rows):
				self[k, j], self[l, j] = self[l, j], self[k, j]
			for i in range(k + 1, self.rows):
				self[i, k] /= self[k, k]
				for j in range(k+1, self.rows):
					self[i, j] -= self[i, k] * self[k, j]
		return self, P

def solvematrixequation(A, b, mode='LUP'):
	if mode not in ['LU', 'LUP']:
		print('Matrix equation solving currently only supports LU/LUP decomposition. (modes \'LU\' and \'LUP\')')
		sys.exit(-1)
	print("A matrix: \n{0}".format(A))
	A, P = A.LUdecomposition() if mode == 'LU' else A.LUPdecomposition()
	print("{0} matrix: \n{1}".format(mode, A))
	print("P matrix: \n{0}".format(P))
	y = A.forwardsubstitution(b, P)
	print("y matrix: \n{0}".format(y))
	x = A.backwardsubstitution(y)
	print("x matrix: \n{0}".format(x))
	return x
