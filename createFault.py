import sys

import Instruction
from Instruction_ARCH import InstructionARM, InstructionAVR, InstructionMIPS, InstructionRISC


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



def main():

    # Récupérations des données
    # Nombre de bits à fauter
    nbBit = int(dataIn[1])
    # Type de faute à effectuer
    faultType = dataIn[2]
    endianess = dataIn[3]
    arch =dataIn[4]

    # Fichier comportant l'instruction
    fileRead = open("instruction.txt", "r")
    # Instruction
    data = fileRead.read()
    instrSTR ,tailleInstr = getInstr(data)
    faultsMatrix=[instrSTR]
    instrInt = string2int(instrSTR)



    #On onvre le template correspondant à l'architecture choisie
    if arch.startswith("arm"):
        instr_obj = InstructionARM(instrSTR, tailleInstr)
    elif arch.startswith("avr"):
        instr_obj = InstructionARM(instrSTR, tailleInstr)
    elif arch.startswith("mips"):
        instr_obj = InstructionARM(instrSTR, tailleInstr)
    elif arch.startswith("risc"):
        instr_obj = InstructionARM(instrSTR, tailleInstr)
    else:
        sys.exit("Architecture non reconnue")

    instr_obj.generateFaults(nbBit,)



    if instr_obj.faultMatrix[-1].startswith('1111') and tailleInstr == 16:
        print(hex(instr_obj.index - 51))
    else:
        print(hex(instr_obj.index - 53))

main()
