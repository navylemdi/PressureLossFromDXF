import numpy as np
import os
from Module import *

deck=parser('/Users/yvan/Desktop/Venture Orbital System/PressureLossFromDXF/testdxf.txt')
path=path(deck, 20e-3)
path.plot()
water=fluid(1000, 1, 120e5, nu=1.007e-6)
system1=system(path, water)
