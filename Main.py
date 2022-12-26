import numpy as np
import os
from Module import *

deck=parser('/Users/yvan/Desktop/Venture Orbital System/Pressure_loss/testdxf.txt')
path=path(deck, 20e-3)
water=fluid(1000, 1, 120e5, nu=1.007e-6)
system1=system(path, water)
print(system1.Qm, 'kg/s')
print(system1.DPTotal, 'Pa')
print(system1.Po*1e-5, 'bar')
