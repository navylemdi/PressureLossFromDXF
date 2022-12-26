import numpy as np
from Module import *

deck=parser('/Users/yvan/Desktop/Venture Orbital System/PressureLossFromDXF/testdxf.txt')
path=path(deck, 20e-3)
water=fluid(1000, 1, 120e5, nu=1.007e-6)
system1=system(path, water)
path.plot()
