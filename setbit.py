import sys
import getopt

#On recupère les arguments depuis le shell
dataIn = sys.argv





#Fonction qui liste les fautes de type setBit
def setbit1(fileWrite,dataTemplate,instrBin,indexWrite, nbBit):
    fileWrite.write(dataTemplate[:indexWrite - 1])
    nbBitInt= int(nbBit)
    for i in range(15, -1+nbBitInt, -1):
        instrFault = instrBin[:i+1-nbBitInt] + nbBitInt*"1" + instrBin[i + 1:]
        #print(instrFault + " : " + instrBin)
        if instrFault != instrBin:
            fileWrite.write(bytes.fromhex(("%04x" % int(instrFault, 2))[2:4]))
            fileWrite.write(bytes.fromhex(("%04x" % int(instrFault, 2))[0:2]))
            indexWrite += 2;
    fileWrite.write(dataTemplate[indexWrite - 1:])
    return indexWrite


#Fonction qui liste les fautes de type resetBit
def resetbit(fileWrite,dataTemplate,instrBin,indexWrite,nbBit):
    fileWrite.write(dataTemplate[:indexWrite - 1])
    nbBitInt = int(nbBit)
    for i in range(15, -1 + nbBitInt, -1):
        instrFault = instrBin[:i + 1 - nbBitInt] + nbBitInt * "0" + instrBin[i + 1:]

        if instrFault != instrBin:
            #print(instrFault + " : " + instrBin)
            fileWrite.write(bytes.fromhex(("%04x" % int(instrFault, 2))[2:4]))
            fileWrite.write(bytes.fromhex(("%04x" % int(instrFault, 2))[0:2]))
            indexWrite += 2;
    fileWrite.write(dataTemplate[indexWrite - 1:])
    return indexWrite


#Fonction qui liste les fautes de type flipBit
def flipbit(fileWrite,dataTemplate,instrBin,indexWrite,nbBit):
    fileWrite.write(dataTemplate[:indexWrite - 1])
    nbBitInt = int(nbBit)
    for i in range(15, -1, -1):
        instrFault = instrBin[:i + 1 - nbBitInt] + ''.join(list(map(lambda y : str(int(not int(y))), instrBin[i +1 -nbBitInt:i+1]))) + instrBin[i + 1:]
        #print(instrFault  +" : "+ instrBin)
        if instrFault != instrBin:
            #print(instrFault + " : " + instrBin)
            fileWrite.write(bytes.fromhex(("%04x" % int(instrFault, 2))[2:4]))
            fileWrite.write(bytes.fromhex(("%04x" % int(instrFault, 2))[0:2]))
            indexWrite += 2;
    fileWrite.write(dataTemplate[indexWrite - 1:])
    return indexWrite





def main():
    #print(dataIn)
    nbBit = dataIn[1]
    faultType = dataIn[2]
    fileRead = open("instruction.txt", "r")
    data = fileRead.read()
    # print(data)
    index = data.find(":")

    instrHex = data[index + 2:index + 6]
    # print(instrHex)
    instrBin = bin(int(instrHex, 16))[2:].zfill(16)
    # print(instrBin)
    fileRead.close()

    fileWrite = open("hexToArm.elf", "wb")
    fileTemplate = open("template.elf", "rb")
    dataTemplate = fileTemplate.read()
    indexWrite = 59
    if faultType == 's':
        indexWrite = setbit1(fileWrite, dataTemplate, instrBin, indexWrite,nbBit)
    elif faultType == 'r':
        indexWrite = resetbit(fileWrite, dataTemplate, instrBin, indexWrite,nbBit)
    elif faultType == 'f':
        indexWrite = flipbit(fileWrite, dataTemplate, instrBin, indexWrite,nbBit)
    fileWrite.close()
    fileTemplate.close()
    print(hex(indexWrite - 53))

main()