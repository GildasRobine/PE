from abc import ABC, abstractmethod
from createFault import string2int, int2string

# Céer un masque de faute de taille nbBit pour une instruction de taille tailleInstr.
# Si on donne un indice de faute, il ne donne que le masque correspondant
# Sinon il génère tous les masques possibles
def maskGenerator(nbBit, tailleInstr, indice=-1):
    masksList=[]
    if indice == -1:
        for i in range(tailleInstr,-1+nbBit,-1):
            mask = tailleInstr*[0]
            mask[i-nbBit:i] = nbBit*[1]
            masksList.append(mask)
    else:
        mask = tailleInstr * [0]
        mask[indice-nbBit:indice] = nbBit*[1]
        masksList.append(mask)
    return masksList

# Pour faire un bit flip.
def xorLoop(instrInt, mask):

    return list(map(lambda x,y: x ^ y, instrInt, mask))


# Pour faire un bit set
def orLoop(instrInt, mask):

    return list(map(lambda x,y: x | y, instrInt, mask))


# Pour faire un bit reset
def andNotLoop(instrInt, mask):

    return list(map(lambda x,y: x & (not y) , instrInt, mask))




class Instruction(ABC):

    def __init__(self, instr, taille):
        self.template
        self.fileWrite
        self.index
        self.instr = instr
        self.taille = taille
        self.maskList = []
        self.faultMatrix = []

    def convert_instr_2int(self):
        instrList = list(self.instr)
        instrIList = list(map(lambda x: int(x, 16), instrList))
        return instrIList

    def writeInELF(self):
        self.fileWrite.write(self.template[:self.index - 1])
        for fault in self.faultMatrix:
            self.convertFault(fault)
            self.index += self.taille // 8
        self.fileWrite.write(self.template[self.index - 1:])
        return self.index

    @abstractmethod
    def convertFault(self, fault):
        pass

    @abstractmethod
    def add_fault(self, fault):
        if fault not in self.faultMatrix:
            self.faultMatrix.append(fault)

    def generateFaults(self, nbBit, faultType, indice=-1):
        self.faultMatrix = [self.instr]
        # On genère les masques
        self.masksList = maskGenerator(nbBit, self.taille, indice)
        instrInt = string2int(self.instr)

        # Selon le type de faute on utilise une des 4 fonctions définies
        for mask in self.masksList:
            if faultType == 's':
                # On genere une faute par masque qu'on ajoute si elle différe de l'instruction de départ ou des fautes déjà existante
                fault = int2string(orLoop(instrInt, mask))
                self.add_fault(self, fault)
            elif faultType == 'r':
                fault = int2string(andNotLoop(instrInt, mask))
                self.add_fault(self, fault)
            elif faultType == 'f':
                fault = int2string(xorLoop(instrInt, mask))
                self.add_fault(self, fault)
        #   On renvoie les fautes générées sans l'instruction de départ

