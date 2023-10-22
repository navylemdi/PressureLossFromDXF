from Module import *
import numpy as np

class system():
    def __init__(self, path, fluid, K=[], Kp=[]):
        """class to create a system

        Args:
            path (_type_): _description_
            fluid (_type_): _description_
            K (list, optional): _description_. Defaults to [].
            Kp (list, optional): _description_. Defaults to [].
        """
        self.Re=self.calc_Re(path, fluid)
        self.K=np.zeros(path.Nb_arcs+path.Nb_lines)
        self.Kp=np.zeros(path.Nb_arcs+path.Nb_lines)
        if K:
            self.K=K
        if Kp:
            self.Kp=Kp
        for i,el in enumerate(path.Entities):
            if el.Type == 'Line':
                if self.Re<=2300 and self.K[i]==0:
                    print('Segment ', i, ': 0 < Re <= 2300 --> Poiseuille OK')
                    self.K[i]=self.Poiseuille()
                if self.Re>=4000 and self.Re<= 100_000 and self.K[i]==0:
                    print('Segment ', i, ': 4000 <= Re <= 100 000 --> Blasius OK')
                    self.K[i] = self.Blasius()
            if el.Type =='Arc' and self.Kp[i]==0:
                print('Calcul arc', i)
                self.Kp[i] = self.Elbow(path, el)
        self.DPline = self.DPline(path, fluid)
        self.DPlineTotal = sum(self.DPline)
        self.DParc = self.DParc(fluid)
        self.DParcTotal = sum(self.DParc)
        self.DPTotal = self.DPlineTotal + self.DParcTotal
        self.Qv = self.Qv(path, fluid)
        self.Qm = self.Qm(path, fluid)
        self.Po = self.Po(fluid)
        
    def calc_Re(self, path, fluid):
        return fluid.V*path.Diameter/(fluid.nu)

    def Poiseuille(self):
        return 64/self.Re

    def Blasius(self):
        return 0.3164*self.Re**-0.25

    def Elbow(self, path, el):
        return np.abs(el.TotalAngle)/np.pi * (0.131+1.847*(path.Diameter/el.radius)**7/2)
    
    def DPline(self, path, fluid):
        return self.K*np.array([i.Length*path.Unit for i in path.Entities])*fluid.rho*(fluid.V**2)/(path.Diameter*2)

    def DParc(self, fluid):
        return self.Kp*fluid.rho*(fluid.V**2)/2
    
    def Qv(self,path,fluid):
        return path.Diameter**2*np.pi*fluid.V/4

    def Qm(self,path, fluid):
        return path.Diameter**2*np.pi*fluid.V/4*fluid.rho

    def Po(self,fluid):
        return fluid.P-self.DPTotal


