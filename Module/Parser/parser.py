import numpy as np
import os

class parser():
    """
    A class to parse DXF file

    Attributes
    ----------
    inputpath : str
        The DXF file path location
    """
    def __init__(self, inputpath):
        """
        Parameters
        ----------
        inputpath : str
            The file location of the deck
        """
        self.inputpath = inputpath
        self.Unit=1 #[m] default unit
        with open(self.inputpath , 'r') as f:
            lines=f.readlines()
            if int(lines[lines.index("$INSUNITS\n")+2]) ==1:
                self.Unit=0.0254
                self.UnitID = 'ft'
            elif int(lines[lines.index("$INSUNITS\n")+2]) ==4:
                self.Unit=10e-3
                self.UnitID = 'mm'
            elif int(lines[lines.index("$INSUNITS\n")+2]) ==5:
                self.Unit=10e-2
                self.UnitID = 'cm'
            elif int(lines[lines.index("$INSUNITS\n")+2]) ==6:
                self.Unit=1
                self.UnitID = 'm'
            print("Length Units in ", self.UnitID)

            StartEntities=lines.index('ENTITIES\n')
            EndEntities=lines[StartEntities:].index('ENDSEC\n')+StartEntities
            Newlist = lines[StartEntities:EndEntities+1]
            self.Nb_lines=Newlist.count('LINE\n')
            self.Nb_arc=Newlist.count('ARC\n')
            
            Index_Droites=[index for index, elem in enumerate(Newlist) if elem=='LINE\n']
            Index_ARC=[index for index, elem in enumerate(Newlist) if elem=='ARC\n']
            
            self.Droite=np.zeros((self.Nb_lines, 7))#6 coordonées pour décrire une droite (2 points)+ 1 donnée d'index 
            for i in range(self.Nb_lines):
                for j in range(6):
                    self.Droite[i, j] = str(Newlist[Index_Droites[i]+12+j*2])
                self.Droite[i, 6] = str(Index_Droites[i])
            self.Arc=np.zeros((self.Nb_arc, 10))#6 coordonées pour décrire un arc (1 centre, un rayon, et angle de début et angle de fin)+ 1 donnée d'index 
            for i in range(self.Nb_arc):
                for j in range(4):
                    self.Arc[i, j] = str(Newlist[Index_ARC[i]+12+j*2])
                self.Arc[i, 4] = str(Newlist[Index_ARC[i]+28])
                self.Arc[i, 5] = str(Newlist[Index_ARC[i]+30])
                self.Arc[i, 6] = str(Index_ARC[i])
                self.Arc[i, 7] = str(Newlist[Index_ARC[i]+20])
                self.Arc[i, 8] = str(Newlist[Index_ARC[i]+22])
                self.Arc[i, 9] = str(Newlist[Index_ARC[i]+24])
            
        f.close()