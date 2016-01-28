import targetfunctions
from math import sqrt

e = 1e-6

def findunimodalinterval(point, step, f):
	l = point - step
	r = point + step

	m = point
	multiplier = 1

	fm = f(point)
	fl = f(l)
	fr = f(r)

	if fm < fr and fm < fl:
		return l, r
	elif fm < fr:
		while True:
			l = m
			m = r
			fm = fr
			r = point + step * multiplier
			multiplier *= 2
			fr = f(r)
			if not fm > fr:
				return r, l
	else:
		while True:
			r = m
			m = l
			fm = fl
			l = point - step * multiplier
			multiplier *= 2
			fl = f(l)
			if not fm > fl:
				return r, l

def goldenratio(a, b, f):
	k = 0.5 * (sqrt(5) - 1)
	c = b - k * (b - a)
	d = a + k * (b - a)
	fc = f(c)
	fd = f(d)
	while (b - a) > e:
		if fc < fd:
			b = d
			d = c
			c = b - k * (b - a)
			fd = fc
			fc = f(c)
		else:
			a = c
			c = d
			d = a + k * (b - a)
			fc = fd
			fd = f(d)
	return (a + b) / 2

def simplex():
	pass

def hookjeeves():
	pass