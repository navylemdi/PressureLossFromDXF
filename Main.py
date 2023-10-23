import numpy as np
from Module import *

deck=parser("textfile.dxf")
trajet=path(deck, Diameter=20e-3)
water=fluid(rho=1000, V=1, Pinlet=120e5, nu=1.007e-6)
print("\u03BC=",water.mu)
system1=system(trajet, water)
print('Perte de charge arcs: ', round(system1.DParcTotal,0), 'Pa')
print('Perte de charge lignes: ', round(system1.DPlineTotal,0), 'Pa')
print('Perte de charge totale: ', round(system1.DPTotal, 0), 'Pa')
trajet.plot()
