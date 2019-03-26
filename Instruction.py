class Instruction:

    def __init__(self, instr, taille):
        self.instr = instr
        self.taille = taille

    def convert_instr_2int(self):
        instrList = list(self.instr)
        instrIList = list(map(lambda x: int(x, 16), instrList))
        return instrIList
