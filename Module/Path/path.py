from Module.Entities import *
import numpy as np
import matplotlib.pyplot as plt

class path():
    def __init__(self, deck, Diameter: float):
        self.Nb_lines=deck.Nb_lines
        self.Nb_arcs=deck.Nb_arc
        self.lines=[]
        self.arcs=[]
        for i in range(self.Nb_lines):
            self.lines.append(line(deck.Droite[i]))
        for j in range(self.Nb_arcs):
            self.arcs.append(arc(deck.Arc[j]))
        self.Entities=np.concatenate((self.arcs, self.lines), axis=0)
        self.Entities= sorted(self.Entities, key=lambda entities:entities.Index)
        self.Diameter=Diameter
        self.Unit=deck.Unit
        self.TotalLength= sum([e.Length for e in self.lines])*self.Unit

    def plot(self):
        fig=plt.figure(0)
        ax=fig.add_subplot(111, projection='3d')
        for i,el in enumerate(self.Entities):
            el.plot(ax,str(i))
        ax.set_xlabel("x axis")
        ax.set_ylabel("y axis")
        ax.set_zlabel("z axis")
        self.set_aspect_equal_3d(ax)
        plt.show()

    def set_aspect_equal_3d(self, ax):
        """
        Parameters
        ----------
        ax : matplotlib.pyplot.axis
            Axis of the 3D plot
        """

        xlim = ax.get_xlim3d()
        ylim = ax.get_ylim3d()
        zlim = ax.get_zlim3d()

        from numpy import mean
        xmean = mean(xlim)
        ymean = mean(ylim)
        zmean = mean(zlim)

        plot_radius = max([abs(lim - mean_)
                        for lims, mean_ in ((xlim, xmean),
                                            (ylim, ymean),
                                            (zlim, zmean))
                        for lim in lims])

        ax.set_xlim3d([xmean - plot_radius, xmean + plot_radius])
        ax.set_ylim3d([ymean - plot_radius, ymean + plot_radius])
        ax.set_zlim3d([zmean - plot_radius, zmean + plot_radius])
    