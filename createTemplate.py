import sys

data = sys.argv

file = open('templatePy.c',"w")

nbNope = int(data[1])

file.write("void main(){ \n asm(")

for i in range(nbNope):
    instr= "\t\"subi R16,$"+str(i)+" ;\" \n"
    file.write(instr)

file.write("); \n}")

file.close()