def writeInELF(file, faultsMatrix, indexWrite, instrTaille, dataTemplate):
    # On ajoute le header du fichier elf
    file.write(dataTemplate[:indexWrite - 1])
    for fault in faultsMatrix:
        # On écrit chaque faute dans le fichier elf
        convertFault(fault,instrTaille,file)
        # On incrémente l'indice en fonction de la taille de l'instruction écrite
        indexWrite += instrTaille//8
    # On ajoute la fin du fichier elf
    file.write(dataTemplate[indexWrite-1:])
    # On renvoie l'index où on s'est arreté
    return indexWrite

def convertFault(fault, instrTaille,file):
    # On convertie la faute au format hexadecimal de taille : instrTaille
    # Des zeros sont ajoutés pour atteindre la taille voulue
    faulthexa= f"{int(fault,2):#0{instrTaille//4+2}x}"[2:]
    # L'ordre d'écriture dépend de l'objdump pour l'architecture ARM
    if instrTaille == 16:

        file.write(bytes.fromhex(faulthexa[2:4]))
        file.write(bytes.fromhex(faulthexa[:2]))
    else:
        file.write(bytes.fromhex(faulthexa[2:4]))
        file.write(bytes.fromhex(faulthexa[:2]))
        file.write(bytes.fromhex(faulthexa[6:8]))
        file.write(bytes.fromhex(faulthexa[4:6]))

def genFault(faults,tailleInstr):
    # Ouverture du template
    fileTemplate = open("templates/templateMIPS", "rb")
    # On fixe l'index à partir duquel on peut écrire dans le fichier ( dépend de l'architecture)
    indexWrite = 65
    dataTemplate = fileTemplate.read()
    fileTemplate.close()
    # Ouverture du fichier dans lequel on va écrire
    fileWrite = open("toObjdump.elf", "wb")
    index = writeInELF(fileWrite, faults, indexWrite, tailleInstr, dataTemplate)
    fileWrite.close()

    return index
