import numpy as np

class arc():
    """
    A class to create line object

    Attributes
    ----------
    Cx: float
        X coordinate (OCS) of the arc center
    Cy: float
        Y coordinate (OCS) of the arc center
    Cz: float
        Z coordinate (OCS) of the arc center
    radius: float
        Radius of the arc
    StartAngle: float
        Start angle of the arc
    EndAngle: float
        End angle of the arc
    Index: int
        Index of the line object in the system
    TotalAngle: float
        Total angle of the arc
    Type: str
        Type of the object
    Length: float
        Length of the arc. By default is 0
    Ez: float
        Z coordinate (WCS) of the arc center
    Ex: float
        X coordinate (WCS) of the arc center
    Ey: float
        Y coordinate (WCS) of the arc center
    StartPoint:
        (X,Y,Z) coordinate (WCS) of the first point of the arc
    EndPoint:
        (X,Y,Z) coordinate (WCS) of the second point of the arc
    CenterPoint:
        (X,Y,Z) coordinate (WCS) of the arc center
    Middle: 
        (X,Y,Z) coordiante (WCS) of the middle point of the arc chord

    Methods
    -------
    calc_total_angle:
        Compute the total angle of the arc
    plot:
        Plot the arc
    from_angle:

    """
    def __init__(self, list):
        """
        Parameters
        ----------
        list : list
            list of ARC attributes
        """
        self.Cx=list[0]
        self.Cy=list[1]
        self.Cz=list[2]
        self.radius=list[3]
        self.StartAngle=list[4]%360
        self.EndAngle=list[5]%360
        self.Index=list[-1]
        self.TotalAngle = self.calc_total_angle()
        self.Type='Arc'
        self.Length=0
        self.Ez=np.array([list[6], list[7], list[8]])/np.linalg.norm(np.array([list[6], list[7], list[8]])) #Extrusion vector
        if (abs(self.Ez[0]) < 1/64.) and (abs(self.Ez[1]) < 1/64.): #Ez est presque aligné avec le Wz du WCS
            v = np.cross(np.array([0, 1, 0]), self.Ez)
            self.Ex = v/np.linalg.norm(v)  # the cross-product operator
        else:
            v=np.cross(np.array([0, 0, 1]), self.Ez)
            self.Ex = v/np.linalg.norm(v)  # the cross-product operator
        self.Ey = np.cross(self.Ez,self.Ex)/np.linalg.norm(np.cross(self.Ez,self.Ex))

        self.Wx = self.wcs_to_ocs((1, 0, 0)) 
        self.Wy = self.wcs_to_ocs((0, 1, 0))
        self.Wz = self.wcs_to_ocs((0, 0, 1))

        self.StartPoint = self.ocs_to_wcs(self.from_deg_angle(self.StartAngle, self.radius) + np.array([self.Cx, self.Cy, self.Cz]))
        self.EndPoint = self.ocs_to_wcs(self.from_deg_angle(self.EndAngle, self.radius) + np.array([self.Cx, self.Cy, self.Cz]))
        self.CenterPoint=self.ocs_to_wcs(np.array([self.Cx, self.Cy, self.Cz]))
        self.Middle = np.array([(self.StartPoint[0]+self.EndPoint[0])/2, (self.StartPoint[1]+self.EndPoint[1])/2, (self.StartPoint[2]+self.EndPoint[2])/2])
    
    def calc_total_angle(self):
        """
        Returns
        -------
        TotalAngle : float
            Total angle of the arc
        """
        return np.abs(self.EndAngle-self.StartAngle)

    def plot(self, ax, i):
        """
        Attributes
        ----------
        ax: Matplotlib.axes object
            axes of the 3D global plot
        i: int
            Index of object
        """
        angle=np.linspace(0,np.radians(self.TotalAngle), 10)
        arc=np.zeros((len(angle), 3))
        for j,a in enumerate(angle):
            arc[j]=self.CenterPoint+(np.sin(np.radians(self.TotalAngle)-a)*(self.StartPoint-self.CenterPoint) + np.sin(a)*(self.EndPoint-self.CenterPoint))/np.sin(np.radians(self.TotalAngle))
        ax.plot(arc[:, 0], arc[:, 1] , arc[:, 2])
        ax.scatter(self.CenterPoint[0], self.CenterPoint[1], self.CenterPoint[2], marker='1')
        ax.text(self.Middle[0], self.Middle[1], self.Middle[2], i)
    
    def from_angle(self, angle, length):
        """
        Compute the coordinates of the a point relative to the arc center.

        Attributes
        ----------
        angle: float
            angle in radians of the point
        length: float
            length to center of the point
        
        Returns
        -------
        Point:
            (X,Y,Z) coordinates (OCS) of a point
        """
        return np.array([np.cos(angle)*length, np.sin(angle)*length, 0.0])

    def from_deg_angle(self, angle, length):
        """
        Compute the coordinates of the a point relative to the arc center.
        
        Attributes
        ----------
        angle: float
            angle in degres of the point
        length: float
            length to center of the point
        
        Returns
        -------
        Point:
            (X,Y,Z) coordinates (OCS) of a point
        """
        return self.from_angle(np.radians(angle), length)

    def wcs_to_ocs(self, P):
        """
        Convert WCS to OCS coordinates of a point
        
        Attributes
        ----------
        P: 
            (X,Y,Z) in WCS coordinates of the point
        
        Returns
        -------
        Point:
            (X,Y,Z) coordinates (OCS) of the point
        """
        px, py, pz = P[0], P[1], P[2]
        x = px * self.Ex[0] + py * self.Ex[1] + pz * self.Ex[2]
        y = px * self.Ey[0] + py * self.Ey[1] + pz * self.Ey[2]
        z = px * self.Ez[0] + py * self.Ez[1] + pz * self.Ez[2]
        return np.array([x, y, z])

    def ocs_to_wcs(self, P):
        """
        Convert OCS to WCS coordinates of a point
        
        Attributes
        ----------
        P: 
            (X,Y,Z) in OCS coordinates of the point
        
        Returns
        -------
        Point:
            (X,Y,Z) coordinates (WCS) of the point
        """
        px, py, pz = P[0], P[1], P[2]
        x = px * self.Wx[0] + py * self.Wx[1] + pz * self.Wx[2]
        y = px * self.Wy[0] + py * self.Wy[1] + pz * self.Wy[2]
        z = px * self.Wz[0] + py * self.Wz[1] + pz * self.Wz[2]
        return np.array([x, y, z])