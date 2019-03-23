def main():
    # Fichier comportant l'instruction à modifier
    fileRead = open("instruction.txt", "r")
    # On récupère l'adresse de l'instruction dans notre fichier texte
    data = fileRead.read()
    addressInstr = data.split(":")[0].replace(" ","")
#On print l'adresse de l'instruction à fauter
    print("0x" + addressInstr)
    fileRead.close()

    # On récupère l'adresse de la fonction contenant l'instruction fautée
    fileRead2 = open("addrFct.txt", "r")
    data2 = fileRead2.read()
    addressCorr = data2.split(" ")[0]
#On print l'adresse de la fonction tampon
    print(hex(int(addressCorr,16)))
    fileRead2.close()

    # On stock le main dans un buffer et on vient ajouter l'instruction fautée dans le fichier
    cFileRead = open("blink32/Src/main.c", "r")
    datacFile = cFileRead.read()
    detectLine = "asm(\"nop;\");\n"

    cFileBuffer = open("blink32/Src/buffer.c", "w")
    cFileBuffer.write(datacFile)

    newInstrFile = open("instructionModif.txt","r")
    dataInstr = newInstrFile.read()

#On récupère l'instruction asm fautée dans le fichier
    newInstr = "asm(\" " +" ".join(dataInstr.split(";")[0].split("\t")[2:]).replace("\n","") + ";\");"

#On remplace le "nop" qui sert de tampon par l'instruction fautée
    chaine = datacFile.replace(detectLine,newInstr)
    newInstrFile.close()
#On met le nouveau programme avec l'instruction fautée dans le main.c
    cFileReadModif = open("blink32/Src/main.c", "w")
    cFileReadModif.write(chaine)


main()

