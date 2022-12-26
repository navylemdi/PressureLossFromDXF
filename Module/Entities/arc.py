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
        self.Ez=np.array([list[7], list[8], list[9]])/np.linalg.norm(np.array([list[7], list[8], list[9]])) #Extrusion vector
        if (abs(self.Ez[0]) < 1/64.) and (abs(self.Ez[1]) < 1/64.):
            v = np.cross(np.array([0, 1, 0]), self.Ez)
            self.Ex = v/np.linalg.norm(v)  # the cross-product operator
        else:
            v=np.cross(np.array([0, 0, 1]), self.Ez)
            self.Ex = v/np.linalg.norm(v)  # the cross-product operator
        self.Ey = np.cross(self.Ez,self.Ex)/np.linalg.norm(np.cross(self.Ez,self.Ex))
        self.Wx = self.wcs_to_ocs((1, 0, 0))
        self.Wy = self.wcs_to_ocs((0, 1, 0))
        self.Wz = self.wcs_to_ocs((0, 0, 1))

        self.StartPoint = self.ocs_to_wcs(self.from_deg_angle(self.StartAngle, self.radius) + np.array([self.Ax, self.Ay, self.Az]))
        self.EndPoint = self.ocs_to_wcs(self.from_deg_angle(self.EndAngle, self.radius) + np.array([self.Ax, self.Ay, self.Az]))
        self.CenterPoint=self.ocs_to_wcs(np.array([self.Ax, self.Ay, self.Az]))
        self.Middle = np.array([(self.StartPoint[0]+self.EndPoint[0])/2, (self.StartPoint[1]+self.EndPoint[1])/2, (self.StartPoint[2]+self.EndPoint[2])/2])
    def calc_total_angle(self):
        return np.abs(self.StartAngle-self.EndAngle)

    def plot(self, ax, i):
        #ax.scatter(self.CenterPoint[0], self.CenterPoint[1], self.CenterPoint[2], marker='+')
        #ax.scatter(self.StartPoint[0], self.StartPoint[1], self.StartPoint[2], marker='+')
        #ax.scatter(self.EndPoint[0], self.EndPoint[1], self.EndPoint[2], marker='+')
        angle=np.linspace(0,np.radians(self.TotalAngle), 10)
        arc=np.zeros((len(angle), 3))
        for j,a in enumerate(angle):
            arc[j]=self.CenterPoint+(np.sin(np.radians(self.TotalAngle)-a)*(self.StartPoint-self.CenterPoint) + np.sin(a)*(self.EndPoint-self.CenterPoint))/np.sin(np.radians(self.TotalAngle))
        ax.plot(arc[:, 0], arc[:, 1] , arc[:, 2])
        ax.text(self.Middle[0], self.Middle[1], self.Middle[2], i)
    
    def from_angle(self, angle, length):
        return np.array([np.cos(angle)*length, np.sin(angle)*length, 0.0])

    def from_deg_angle(self, angle, length):
        return self.from_angle(np.radians(angle), length)

    def wcs_to_ocs(self, P):
        px, py, pz = P[0], P[1], P[2]
        x = px * self.Ex[0] + py * self.Ex[1] + pz * self.Ex[2]
        y = px * self.Ey[0] + py * self.Ey[1] + pz * self.Ey[2]
        z = px * self.Ez[0] + py * self.Ez[1] + pz * self.Ez[2]
        return np.array([x, y, z])

    def ocs_to_wcs(self, P):
        px, py, pz = P[0], P[1], P[2]
        x = px * self.Wx[0] + py * self.Wx[1] + pz * self.Wx[2]
        y = px * self.Wy[0] + py * self.Wy[1] + pz * self.Wy[2]
        z = px * self.Wz[0] + py * self.Wz[1] + pz * self.Wz[2]
        return np.array([x, y, z])