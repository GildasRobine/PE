import Instruction


class InstructionARM(Instruction):

    def __init__(self, instr, taille):
        super.__init__(self,instr, taille)
        self.template = open("templates/templateARM", "rb")
        self.index = 59
        self.fileWrite = open("toObjdump.elf", "wb")


    def convertFault(self, fault):
        faulthexa = f"{int(fault, 2):#0{self.taille// 4 + 2}x}"[2:]
        if self.taille == 16:
            self.fileWrite.write(bytes.fromhex(faulthexa[2:4]))
            self.fileWrite.write(bytes.fromhex(faulthexa[:2]))
        else:
            self.fileWrite.write(bytes.fromhex(faulthexa[2:4]))
            self.fileWrite.write(bytes.fromhex(faulthexa[:2]))
            self.fileWrite.write(bytes.fromhex(faulthexa[6:8]))
            self.fileWrite.write(bytes.fromhex(faulthexa[4:6]))

    def add_fault(self, fault):
        if fault not in self.faultsMatrix:
            # Gestion du changement de taille de l'instruction ARM
            # Une instruction 16 bits ne commence jamais par 111XX sauf 11100
            if self.taille == 16 and (fault[0:3] == "111" and fault[0:5] != '11100'):
                print("16to32:" + hex(int(fault, 2)))
            elif self.taille == 32 and (fault[0:3] != "111" or fault[0:5] == '11100'):
                print("32to16:" + hex(int(fault[0:16], 2)) + hex(int(fault[16:32], 2)))
            else:
                self.faultsMatrix.append(fault)

class InstructionAVR(Instruction):

    def __init__(self, instr, taille):
        super.__init__(self,instr, taille)
        self.template = open("templates/templateAVR", "rb")
        self.index = 59
        self.fileWrite = open("toObjdump.elf", "wb")

    def convertFault(self, fault):
        faulthexa = f"{int(fault, 2):#0{self.taille// 4 + 2}x}"[2:]
        self.fileWrite.write(bytes.fromhex(faulthexa))


class InstructionRISC(Instruction):

    def __init__(self, instr, taille):
        super.__init__(self,instr, taille)
        self.template = open("templates/templateRISC", "rb")
        self.index = 71
        self.fileWrite = open("toObjdump.elf", "wb")

    def convertFault(self, fault):
        faulthexa = f"{int(fault, 2):#0{self.taille // 4 + 2}x}"[2:]
        if self.taille == 16:

            self.fileWrite.write(bytes.fromhex(faulthexa[2:4]))
            self.fileWrite.write(bytes.fromhex(faulthexa[:2]))
        else:
            self.fileWrite.write(bytes.fromhex(faulthexa[6:8]))
            self.fileWrite.write(bytes.fromhex(faulthexa[4:6]))
            self.fileWrite.write(bytes.fromhex(faulthexa[2:4]))
            self.fileWrite.write(bytes.fromhex(faulthexa[:2]))


class InstructionMIPS(Instruction):

    def __init__(self, instr, taille):
        super.__init__(self,instr, taille)
        self.template = open("templates/templateMIPS", "rb")
        self.index = 65
        self.fileWrite = open("toObjdump.elf", "wb")

    def convertFault(self, fault):
        faulthexa = f"{int(fault, 2):#0{self.taille// 4 + 2}x}"[2:]
        if self.taille == 16:

            self.fileWrite.write(bytes.fromhex(faulthexa[2:4]))
            self.fileWrite.write(bytes.fromhex(faulthexa[:2]))
        else:
            self.fileWrite.write(bytes.fromhex(faulthexa[2:4]))
            self.fileWrite.write(bytes.fromhex(faulthexa[:2]))
            self.fileWrite.write(bytes.fromhex(faulthexa[6:8]))
            self.fileWrite.write(bytes.fromhex(faulthexa[4:6]))
