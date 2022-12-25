import sys

class fluid():
    def __init__(self, rho, V, Pinlet, mu=0, nu=0):
        self.rho=rho
        self.V=V
        self.P=Pinlet
        if mu ==0 and nu ==0:
            print('Erreur : mu ou nu doivent être caractérisée')
            sys.exit(1)
        if mu==0:
            self.nu=nu
            self.mu=self.rho*self.nu
        if nu==0:
            self.mu=mu
            self.nu=self.mu*self.rho