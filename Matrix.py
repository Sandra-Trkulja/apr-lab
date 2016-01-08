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
				exit(-1)
			result = [[sum(self[i, k] * other[k, j] for k in range(self.cols)) for j in range(other.cols)] for i in range(self.rows)]
			return Matrix(result)

	def __rmul__(self, other):
		return Matrix.__mul__(self, other)

	def __invert__(self): #used for transposin
		result = [[self[i, j] for i in range(self.rows)] for j in range(self.cols)]
		return Matrix(result)

	def __eq__(self, other):
		self._checkdimensions(other)
		eps = 0.00001
		for i in range(self.rows):
			for j in range(self.cols):
				if abs(self[i, j] - other[i, j]) < eps:
					return False
		return True

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
			exit(-1)
		return

	def _checkaccess(self, x, y):
		if x < 0 or x >= self.rows or y < 0 or y >= self.cols:
			print('Cannot access element ({0},{1}) because it is out of the range ({2},{3}).'.format(x, y, self.rows, self.cols))
			exit(-1)
		return

	def printtofile(self, filename):
		with open(filename, 'w') as f:
			print("\n".join([' '.join([str(x) for x in row]) for row in self.m]), file=f)

	def printpretty(self, width=7, precision=2):
		print('\n'.join([''.join(['{0:{1}.{2}f}'.format(item, width, precision) for item in row]) for row in self.m]))
