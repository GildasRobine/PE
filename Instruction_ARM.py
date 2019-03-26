import Instruction


class Instruction_ARM(Instruction):

    def __init__(self, instr, taille):
        super.__init__(self,instr, taille)
        self.template = open("templates/templateARM", "rb")
        self.indexW = 59
        self.fileWrite = open("toObjdump.elf", "wb")


    def convertFault(self):
        faulthexa = f"{int(self.instr, 2):#0{self.taille// 4 + 2}x}"[2:]
        if self.taille == 16:

            self.fileWrite.write(bytes.fromhex(faulthexa[2:4]))
            self.fileWrite.write(bytes.fromhex(faulthexa[:2]))
        else:
            self.fileWrite.write(bytes.fromhex(faulthexa[2:4]))
            self.fileWrite.write(bytes.fromhex(faulthexa[:2]))
            self.fileWrite.write(bytes.fromhex(faulthexa[6:8]))
            self.fileWrite.write(bytes.fromhex(faulthexa[4:6]))
