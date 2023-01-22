import numpy as np

class line():
    """
    A class to create line object

    Attributes
    ----------
    Ax: float
        X coordinate (WCS) of the first point
    Ay: float
        Y coordinate (WCS) of the first point
    Az: float
        Z coordinate (WCS) of the first point
    Bx: float
        X coordinate (WCS) of the second point
    By: float
        Y coordinate (WCS) of the second point
    Bz: float
        Z coordinate (WCS) of the second point
    Index:
        Index of the line object in the system
    Length:
        Length of the line
    Type:
        Type of the object
    Middle:
        (X,Y,Z) coordinate (WCS) of the middle point of the line
    
    Methods
    -------
    calc_length:
        Compute the length of the line
    plot:
        Plot the line
    """

    def __init__(self, list):
        """
        Parameters
        ----------
        list : list
            list of LINE attributes
        """
        self.Ax=list[0]
        self.Ay=list[1]
        self.Az=list[2]
        self.Bx=list[3]
        self.By=list[4]
        self.Bz=list[5]
        self.Index=list[6]
        self.Length=self.calc_length()
        self.Type='Line'
        self.Middle = np.array([(self.Ax+self.Bx)/2, (self.Ay+self.By)/2, (self.Az+self.Bz)/2])

    def calc_length(self):
        """
        Returns
        -------
        Length:
            Length of the line
        """
        return np.sqrt((self.Ax-self.Bx)**2 + (self.Ay-self.By)**2 + (self.Az-self.Bz)**2)
    
    def plot(self, ax, i):
        """
        Attributes
        ----------
        ax: Matplotlib.axes object
            axes of the 3D global plot
        i: int
            Index of object
        """
        ax.scatter([self.Ax, self.Bx], [self.Ay, self.By], [self.Az, self.Bz], marker='+')
        ax.plot([self.Ax, self.Bx], [self.Ay, self.By], [self.Az, self.Bz])
        ax.text(self.Middle[0], self.Middle[1], self.Middle[2], i)
