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
                self.Unit=1e-3
                self.UnitID = 'mm'
            elif int(lines[lines.index("$INSUNITS\n")+2]) ==5:
                self.Unit=1e-2
                self.UnitID = 'cm'
            elif int(lines[lines.index("$INSUNITS\n")+2]) ==6:
                self.Unit=1
                self.UnitID = 'm'
            print("Length Units in ", self.UnitID)

            StartEntities=lines.index('ENTITIES\n') #Index de début de la section ENTITIES
            EndEntities=lines[StartEntities:].index('ENDSEC\n')+StartEntities #Index de fin de la section ENTITIES 
            Entities = lines[StartEntities:EndEntities+1] #Liste d'entitées
            self.Nb_lines=Entities.count('LINE\n') #Nombre d'éléments LINE
            self.Nb_arc=Entities.count('ARC\n') #Nombre d'éléments ARC
            
            Index_Droites=[index for index, elem in enumerate(Entities) if elem=='LINE\n']
            Index_ARC=[index for index, elem in enumerate(Entities) if elem=='ARC\n']
            
            Attributs_droite=[' 10\n', ' 20\n', ' 30\n', ' 11\n', ' 21\n', ' 31\n']
            Attributs_arc=[' 10\n', ' 20\n', ' 30\n', ' 40\n', ' 50\n', ' 51\n', '210\n', '220\n', '230\n']
            self.Droite=np.zeros((self.Nb_lines, 7))#6 coordonées pour décrire une droite (2 points 3D)+ 1 donnée d'index 
            for i in range(self.Nb_lines-1):
                for j,att in enumerate(Attributs_droite):
                    self.Droite[i, j] = str(Entities[Entities[Index_Droites[i]:Index_Droites[i+1]].index(att)+1+Index_Droites[i]])
                self.Droite[i, 6] = str(Index_Droites[i])
            for j,att in enumerate(Attributs_droite):
                self.Droite[-1, j] = str(Entities[Entities[Index_Droites[-1]:2*Index_Droites[-1]-Index_Droites[-2]].index(att)+1+Index_Droites[-1]])
            self.Droite[-1, 6] = str(Index_Droites[-1])

            self.Arc=np.zeros((self.Nb_arc, 10))#6 coordonées pour décrire un arc (1 centre, un rayon, et angle de début et angle de fin) + 3 données de sens d'extrusion + 1 donnée d'index 
            for i in range(self.Nb_arc-1):
                for j,att in enumerate(Attributs_arc):
                    self.Arc[i,j] = str(Entities[Entities[Index_ARC[i]:Index_ARC[i+1]].index(att)+1+Index_ARC[i]])
                self.Arc[i, 9] = str(Index_ARC[i])
            for j,att in enumerate(Attributs_arc):
                self.Arc[-1,j] = str(Entities[Entities[Index_ARC[-1]:2*Index_ARC[-1]-Index_ARC[-2]].index(att)+1+Index_ARC[-1]])
            self.Arc[-1, 9] = str(Index_ARC[-1])
                # for j in range(4):
                #     self.Arc[i, j] = str(Entities[Index_ARC[i]+12+j*2])
                # self.Arc[i, 4] = str(Entities[Index_ARC[i]+28])
                # self.Arc[i, 5] = str(Entities[Index_ARC[i]+30])
                # self.Arc[i, 6] = str(Index_ARC[i])
                # self.Arc[i, 7] = str(Entities[Index_ARC[i]+20])
                # self.Arc[i, 8] = str(Entities[Index_ARC[i]+22])
                # self.Arc[i, 9] = str(Entities[Index_ARC[i]+24])
            
        f.close()