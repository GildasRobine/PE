import sys
import getopt

dataIn = sys.argv





def setbit1(fileWrite,dataTemplate,instrBin,indexWrite):
    fileWrite.write(dataTemplate[:indexWrite - 1])
    for i in range(15, -1, -1):
        instrFault = instrBin[:i] + "1" + instrBin[i + 1:]
        print(instrFault + " : " + instrBin)
        if instrFault != instrBin:
            fileWrite.write(bytes.fromhex(hex(int(instrFault, 2))[4:6]))
            fileWrite.write(bytes.fromhex(hex(int(instrFault, 2))[2:4]))
            indexWrite += 2;
    fileWrite.write(dataTemplate[indexWrite - 1:])
    return indexWrite

def resetbit(fileWrite,dataTemplate,instrBin,indexWrite):
    fileWrite.write(dataTemplate[:indexWrite - 1])
    for i in range(15, -1, -1):
        instrFault = instrBin[:i] + "0" + instrBin[i + 1:]

        if instrFault != instrBin:
            #print(instrFault + " : " + instrBin)
            fileWrite.write(bytes.fromhex(("%04x" % int(instrFault,2))[2:4]))
            fileWrite.write(bytes.fromhex(("%04x" % int(instrFault,2))[0:2]))
            indexWrite += 2;
    fileWrite.write(dataTemplate[indexWrite - 1:])
    return indexWrite

def flipbit(fileWrite,dataTemplate,instrBin,indexWrite):
    fileWrite.write(dataTemplate[:indexWrite - 1])
    for i in range(15, -1, -1):
        instrFault = instrBin[:i] + str(int(not int(instrBin[i]))) + instrBin[i + 1:]
        #print(instrFault  +" : "+ instrBin)
        if instrFault != instrBin:
            #print(instrFault + " : " + instrBin)
            fileWrite.write(bytes.fromhex(("%04x" % int(instrFault,2))[2:4]))
            fileWrite.write(bytes.fromhex(("%04x" % int(instrFault,2))[0:2]))
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
    if nbBit == '1':
        if faultType == 's':
            indexWrite = setbit1(fileWrite, dataTemplate, instrBin, indexWrite)
        elif faultType == 'r':
            indexWrite = resetbit(fileWrite, dataTemplate, instrBin, indexWrite)
        elif faultType == 'f':
            indexWrite = flipbit(fileWrite, dataTemplate, instrBin, indexWrite)
    fileWrite.close()
    fileTemplate.close()
    print(hex(indexWrite - 53))

main()