import numpy as np
from Module import *

deck=parser('/Users/yvan/Desktop/Venture Orbital System/PressureLossFromDXF/testdxf.txt')
trajet=path(deck, Diameter=20e-3)
water=fluid(rho=1000, V=1, Pinlet=120e5, nu=1.007e-6)
print(water.mu)
system1=system(trajet, water)
print(system1.DPlineTotal)
trajet.plot()
