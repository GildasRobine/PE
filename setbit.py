fileRead = open("instruction.txt","r")
data = fileRead.read()
#print(data)
index = data.find(":")

instrHex = data[index+2:index+6]
#print(instrHex)
instrBin = bin(int(instrHex,16))[2:].zfill(16)
#print(instrBin)
fileRead.close()

fileWrite = open("hexToArm.elf","wb")
fileTemplate = open("template.elf","rb")
dataTemplate = fileTemplate.read()
indexWrite = 59

fileWrite.write(dataTemplate[:indexWrite-1])
for i in range(15,-1,-1):
    instrFault = instrBin[:i]+"1"+instrBin[i+1:]
    if instrFault != instrBin:
        fileWrite.write(bytes.fromhex(hex(int(instrFault,2))[4:6]))
        fileWrite.write(bytes.fromhex(hex(int(instrFault, 2))[2:4]))
        indexWrite += 2;
fileWrite.write(dataTemplate[indexWrite-1:])
fileWrite.close()
fileTemplate.close()
print(hex(indexWrite-53))


