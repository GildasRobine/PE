import sys

# On recupère les arguments depuis le shell
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

def generateFaults(instrSTR, nbBit, faultType, tailleInstr, indice = -1):
    faultsMatrix=[instrSTR]
    # On genère les masques
    masksList = maskGenerator(nbBit,tailleInstr,indice)
    instrInt = string2int(instrSTR)

    # Selon le type de faute on utilise une des 4 fonctions définies
    if faultType == 's':
        for mask in masksList:
            # On genere une faute par masque qu'on ajoute si elle différe de l'instruction de départ ou des fautes déjà existante
            fault = int2string(orLoop(instrInt,mask))
            faultsMatrix = sizeChange(faultsMatrix, fault, tailleInstr)
    elif faultType == 'r':
        for mask in masksList:
            fault = int2string(andNotLoop(instrInt, mask))
            faultsMatrix = sizeChange(faultsMatrix,fault, tailleInstr)
    elif faultType == 'f':
        for mask in masksList:
            fault = int2string(xorLoop(instrInt, mask))
            faultsMatrix = sizeChange(faultsMatrix,fault, tailleInstr)
#   On renvoie les fautes générées sans l'instruction de départ
    return faultsMatrix[1:]

def sizeChange(faultsMatrix,fault, tailleInstr):
    if fault not in faultsMatrix:
        # Gestion du changement de taille de l'instruction ARM
        # Une instruction 16 bits ne commence jamais par 111XX sauf 11100
        if (tailleInstr == 16 and (fault[0:3] == "111" and fault[0:5]!='11100')):
            print("16to32:" + hex(int(fault, 2)))
        elif (tailleInstr == 32 and (fault[0:3] != "111" or fault[0:5]=='11100')):
            print("32to16:" + hex(int(fault[0:16], 2)) + hex(int(fault[16:32], 2)))
        else:
            faultsMatrix.append(fault)
    return faultsMatrix

def getInstr(data):
    # recupere l'instruction hexadeciaml
    instrHex = data.split("\t")[1]

    instrHex = instrHex.replace(" ", "")
    instrList= list(instrHex)
    #Calcul de la taille de l'instruction
    tailleInstr=len(instrList)*4

    # la convertie en une chaine de 0 et 1
    instrBin = (bin(int(instrHex,16))[2:]).zfill(tailleInstr)
    return instrBin, tailleInstr

def writeInELF(file, faultsMatrix, indexWrite, instrTaille, dataTemplate, endianess, arch):
    file.write(dataTemplate[:indexWrite - 1])
    for fault in faultsMatrix:
        convertFault(fault,instrTaille,file,endianess, arch)
        indexWrite += instrTaille//8
    file.write(dataTemplate[indexWrite-1:])
    return indexWrite

def convertFault(fault, instrTaille,file,endianess, arch):
    faulthexa= f"{int(fault,2):#0{instrTaille//4+2}x}"[2:]
    if endianess=='le':
        if instrTaille == 16:

            file.write(bytes.fromhex(faulthexa[2:4]))
            file.write(bytes.fromhex(faulthexa[:2]))
        else:
            if arch.startswith("risc"):
                file.write(bytes.fromhex(faulthexa[6:8]))
                file.write(bytes.fromhex(faulthexa[4:6]))
                file.write(bytes.fromhex(faulthexa[2:4]))
                file.write(bytes.fromhex(faulthexa[:2]))
            else:
                file.write(bytes.fromhex(faulthexa[2:4]))
                file.write(bytes.fromhex(faulthexa[:2]))
                file.write(bytes.fromhex(faulthexa[6:8]))
                file.write(bytes.fromhex(faulthexa[4:6]))
    else:
        file.write(bytes.fromhex(faulthexa))



def main():

    # Récupérations des données
    # Nombre de bits à fauter
    nbBit = int(dataIn[1])
    # Type de faute à effectuer
    faultType = dataIn[2]
    endianess = dataIn[3]
    arch =dataIn[4]
    #On onvre le template correspondant à l'architecture choisie
    if arch.startswith("arm"):
        fileTemplate = open("templates/templateARM", "rb")
        indexWrite = 59
    elif arch.startswith("avr"):
        fileTemplate = open("templates/templateAVR", "rb")
        indexWrite = 59
    elif arch.startswith("mips"):
        fileTemplate = open("templates/templateMIPS", "rb")
        indexWrite = 65
    elif arch.startswith("risc"):
        fileTemplate = open("templates/templateRISC", "rb")
        indexWrite = 71

    dataTemplate = fileTemplate.read()
    fileTemplate.close()
    fileWrite = open("toObjdump.elf", "wb")


    # Fichier comportant l'instruction
    fileRead = open("instruction.txt", "r")
    # Instruction
    data = fileRead.read()
    instrSTR ,tailleInstr = getInstr(data)

    faults = generateFaults(instrSTR, nbBit, faultType, tailleInstr)
    index = writeInELF(fileWrite, faults, indexWrite, tailleInstr, dataTemplate, endianess, arch)
    if faults[-1].startswith('1111') and tailleInstr == 16:
        print(hex(index-51))
    else:
        print(hex(index - 53))
    fileWrite.close()

main()
