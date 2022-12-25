import numpy as np

class line():
    def __init__(self, list):
        self.Ax=list[0]
        self.Ay=list[1]
        self.Az=list[2]
        self.Bx=list[3]
        self.By=list[4]
        self.Bz=list[5]
        self.Index=list[6]
        self.Length=self.calc_length()
        self.Type='Line'


    def calc_length(self):
        return np.sqrt((self.Ax-self.Bx)**2 + (self.Ay-self.By)**2 + (self.Az-self.Bz)**2)