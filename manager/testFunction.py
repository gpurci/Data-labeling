# !/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np


def PlotAlg(x, d1, d2, d3):
	print("x ", x)
	axe = np.arange(x)
	print("axe ", axe)
	# red dashes, blue squares and green triangles
	plt.plot(axe, d1, 'ro', axe, d2, 'bs', axe, d3, 'g^')
	plt.show()

# Const = 6.106
# x = 30

# d1 = np.zeros((x))
# d2 = np.zeros((x))
# d3 = np.zeros((x))

# for i in range(x):
# 	d1[i] = 1. / ((i + 1)**(i + 1))
# 	d2[i] = 1 + (1. / (2**(i + 1)))
# 	d3[i] = 1.5 + (1. / ((i + 1)**(i + 1)))

# print("d1 ", d1)
# print("d2 ", d2)
# print("d3 ", d3)

# PlotAlg(x, d1, d2, d3)
d = DistantaDouaPuncte(0, 5.9268988361, 1, 7.34790637354)
print("distanta ", d)
print("distanta ", DistantaDouaPuncte(0, 5.9268988361, 1, 8.94257243764))
print("distanta ", DistantaDouaPuncte(0, 5.9268988361, 1, 10.64025952))

d = DistantaDouaPuncte(0, 8.54398761302, 1, 9.89307406828)
print("distanta 1", d)
print("distanta 1", DistantaDouaPuncte(0, 8.54398761302, 1, 11.4268228221))
print("distanta 1", DistantaDouaPuncte(0, 8.54398761302, 1, 13.0803477836))

d = DistantaDouaPuncte(0, 8.67298499987, 1, 10.1425114925)
print("distanta 2", d)
print("distanta 2", DistantaDouaPuncte(0, 8.67298499987, 1, 11.7673084154))
print("distanta 2", DistantaDouaPuncte(0, 8.67298499987, 1, 13.4844202438))


print("Angle ", AnglePoint(0, 5.9268988361, 28, 58.2050789837))
print("Angle ", AnglePoint(0, 5.9268988361, 1, 7.34790637354))
print("Angle ", AnglePoint(0, 5.9268988361, 27, 56.2594369885))
print("Angle ", AnglePoint(0, 5.9268988361, 1, 7.34790637354))
