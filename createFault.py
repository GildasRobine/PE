import sys
from forARCH import forRISC, forARM, forAVR, forMIPS

# On recupère les arguments envoyés depuis le shell
dataIn = sys.argv


# Convertie une chaine de caractère composée de 0 et de 1 en une liste d'entier (0 ou 1)
def string2int(instrSTR):
    instrList = list(instrSTR)
    instrIList = list(map(lambda x: int(x,16), instrList))

    return instrIList


# Convertie une liste d'entier (0 ou 1), instrInt, en une chaine de caractère composée de 0 et de 1, "".join(instrSTRList).
def int2string(instrInt):
    instrList = list(instrInt)
    instrSTRList = list(map(lambda x: str(int(x)), instrList))

    return "".join(instrSTRList)

# Céer un masque de faute de taille nbBit pour une instruction de taille tailleInstr.
# Si on donne un indice de faute, il ne donne que le masque correspondant ( pas implémenté pour le moment)
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
        if (nbBit+indice<tailleInstr):
            mask[indice:indice+nbBit] = nbBit*[1]
        else:
            mask[indice:] = (tailleInstr-indice)*[1]
        masksList.append(mask)
    return masksList

# Pour faire un bit flip.
def xorLoop(instrInt, mask):
    # instruction XOR masque
    return list(map(lambda x,y: x ^ y, instrInt, mask))


# Pour faire un bit set
def orLoop(instrInt, mask):
    # instruction OR masque
    return list(map(lambda x,y: x | y, instrInt, mask))


# Pour faire un bit reset
def andNotLoop(instrInt, mask):
    # instruction AND NOT(masque)
    return list(map(lambda x,y: x & (not y) , instrInt, mask))


def generateFaults(instrSTR, nbBit, faultType, tailleInstr, arch, indice = -1):
    faultsMatrix=[instrSTR]
    # On genère les masques
    masksList = maskGenerator(nbBit,tailleInstr,indice)
    instrInt = string2int(instrSTR)

    # Selon le type de faute on utilise une des 4 fonctions définies
    if faultType == 's':
        for mask in masksList:
            # On genere une faute par masque qu'on ajoute si elle différe de l'instruction de départ ou des fautes déjà existante
            fault = int2string(orLoop(instrInt,mask))
            faultsMatrix = add_to_faults_list(faultsMatrix, fault, tailleInstr, arch)
    elif faultType == 'r':
        for mask in masksList:
            fault = int2string(andNotLoop(instrInt, mask))
            faultsMatrix = add_to_faults_list(faultsMatrix, fault, tailleInstr, arch)
    elif faultType == 'f':
        for mask in masksList:
            fault = int2string(xorLoop(instrInt, mask))
            faultsMatrix = add_to_faults_list(faultsMatrix, fault, tailleInstr, arch)
#   On renvoie les fautes générées sans l'instruction de départ
    return faultsMatrix[1:]


def add_to_faults_list(faultsMatrix, fault, tailleInstr, arch):
    # On vérifie que la faute donne bien une nouvelle instruction
    if fault not in faultsMatrix:
        # Gestion du changement de taille de l'instruction ARM
        # Une instruction 16 bits ne commence jamais par 111XX sauf 11100
        if arch.startswith("arm"):
            if (tailleInstr == 16 and (fault[0:3] == "111" and fault[0:5]!='11100')):
                print("16to32:" + hex(int(fault, 2)))
            elif (tailleInstr == 32 and (fault[0:3] != "111" or fault[0:5]=='11100')):
                print("32to16:" + hex(int(fault[0:16], 2)) + hex(int(fault[16:32], 2)))
            else:
                faultsMatrix.append(fault)
        else:
            faultsMatrix.append(fault)
    return faultsMatrix



def getInstr(data):
    # recupere l'instruction hexadeciaml
    # Objdump sépare ses champs par une tabulation
    instrHex = data.split("\t")[1]

    instrHex = instrHex.replace(" ", "")
    instrList= list(instrHex)
    #Calcul de la taille de l'instruction
    tailleInstr=len(instrList)*4

    # la convertie en une chaine de 0 et 1 et complete avec des 0 à gauches
    instrBin = (bin(int(instrHex,16))[2:]).zfill(tailleInstr)
    return instrBin, tailleInstr



def main():

    # Récupérations des données
    # Nombre de bits à fauter
    nbBit = int(dataIn[1])
    # Type de faute à effectuer
    faultType = dataIn[2]
    #Architecture
    arch =dataIn[3]

    indiceFault = int(dataIn[4])

    # Fichier comportant l'instruction
    fileRead = open("instruction.txt", "r")
    # Instruction et sa taille
    data = fileRead.read()
    instrSTR ,tailleInstr = getInstr(data)
    #Generation des fautes
    faults = generateFaults(instrSTR, nbBit, faultType, tailleInstr, arch, indiceFault)

    # On genère les fautes avec ouverture des templates et récupération de l'index en fonction de l'architecture
    # Si l'architecture donnée n'est pas reconnue le système sort avec une erreur
    if arch.startswith("arm"):
        index = forARM.genFault(faults, tailleInstr)
    elif arch.startswith("avr"):
        index = forAVR.genFault(faults, tailleInstr)
    elif arch.startswith("mips"):
        index = forMIPS.genFault(faults, tailleInstr)
    elif arch.startswith("risc"):
        index = forRISC.genFault(faults, tailleInstr)
    else:
        sys.exit("Architecture non reconnue")


    # On retourne l'indice au shell pour l'objdump
    print(hex(index-51))

main()
