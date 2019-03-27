def writeInELF(file, faultsMatrix, indexWrite, instrTaille, dataTemplate):
    file.write(dataTemplate[:indexWrite - 1])
    for fault in faultsMatrix:
        convertFault(fault,instrTaille,file)
        indexWrite += instrTaille//8
    file.write(dataTemplate[indexWrite-1:])
    return indexWrite

def convertFault(fault, instrTaille,file):
    faulthexa= f"{int(fault,2):#0{instrTaille//4+2}x}"[2:]
    if instrTaille == 16:
        # L'ordre d'écriture dépend de l'objdump pour l'architecture ARM
        file.write(bytes.fromhex(faulthexa[2:4]))
        file.write(bytes.fromhex(faulthexa[:2]))
    else:
        file.write(bytes.fromhex(faulthexa[6:8]))
        file.write(bytes.fromhex(faulthexa[4:6]))
        file.write(bytes.fromhex(faulthexa[2:4]))
        file.write(bytes.fromhex(faulthexa[:2]))


def genFault(faults,tailleInstr):
    # Ouverture du template
    fileTemplate = open("templates/templateRISC", "rb")
    # On fixe l'index à partir duquel on peut écrire dans le fichier ( dépend de l'architecture)
    indexWrite = 71
    dataTemplate = fileTemplate.read()
    fileTemplate.close()
    # Ouverture du fichier dans lequel on va écrire
    fileWrite = open("toObjdump.elf", "wb")
    index = writeInELF(fileWrite, faults, indexWrite, tailleInstr, dataTemplate)
    fileWrite.close()

    return index