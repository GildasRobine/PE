import sys

data = sys.argv

file = open('templatePy.c',"w")

nbNope = int(data[1])

file.write("void main(){ \n asm{")

for i in range(nbNope):
    file.write("\t\"nop\" \n")

file.write("} \n}")

file.close()