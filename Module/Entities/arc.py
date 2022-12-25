import numpy as np

class arc():
    def __init__(self, list):
        self.Ax=list[0]
        self.Ay=list[1]
        self.Az=list[2]
        self.radius=list[3]
        self.StartAngle=list[4]
        self.EndAngle=list[5]
        self.Index=list[6]
        self.TotalAngle = self.calc_total_angle()
        self.Type='Arc'
        self.Length=0

    def calc_total_angle(self):
        return np.abs(self.StartAngle-self.EndAngle)