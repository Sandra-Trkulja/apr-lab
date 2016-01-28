from math import pow
from math import sqrt
from math import sin

def counted(fn):
    def wrapper(*args, **kwargs):
        wrapper.called+= 1
        return fn(*args, **kwargs)
    wrapper.called= 0
    wrapper.__name__= fn.__name__
    return wrapper

@counted
def f1(l):
	# Rosenbrock banana function
	x, y = l
	return 100 * pow(y - pow(x, 2), 2) + pow(1 - x, 2)

@counted
def f2(l):
	x, y = l
	return pow(x - 4, 2) + 4 * pow(y - 2, 2)

@counted
def f3(l):
	return sum([pow(xi - i, 2) for i, xi in enumerate(l)])

@counted
def f4(l):
	x, y = l
	return abs((x - y) * (x + y)) + sqrt(pow(x, 2) + pow(x, 2))

@counted
def f6(l):
	# Schaffer's function f6
	s = sum([pow(x, 2) for x in l])
	num = pow(sin(s), 2) - 0.5
	denom = pow(1 + 0.001 * s, 2)
	return 0.5 + num / denom

def f1startpoint():
	return [-1.9, 2]

def f2startpoint():
	return [0.1, 0.3]

def f3startpoint(dim):
	return [0] * dim

def f4startpoint():
	return [5.1, 1.1]

def f6startpoint(dim):
	return [0] * dim