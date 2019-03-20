#!/bin/bash

echo "Création du ficheir template"
read -p "Entrez la taille des isntructions (16 ou 32 bits) : " size

if [ $size -eq 16 ]; then
    echo "$size"
    python3 ./createTemplate.py 16
else
    echo "$size"
    # le nop étant sur 16 bits il en faut 64 pour avoir la place de faire 32 instructions sur 32 bits
    python3 ./createTemplate.py 64
fi

toolchain=$1
echo "Compilation du template"
${toolchain}gcc -c -mcpu=cortex-m3 templatePy.c -o templatePy

echo "Compilation réussie"
