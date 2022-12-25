from Module import *
import numpy as np

class path():
    def __init__(self, deck, Diameter):
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
    def pressure_loss(self):
        return None
    