#!/bin/bash

echo "Création du fichier template"
read -p "Entrez la taille des instructions (16 ou 32 bits) : " size

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
case $toolchain in
    arm*) optionARCH=-mcpu=cortex-m3;;
    avr*) optionARCH=-mmcu=avr4;;
    mips*) optionARCH= ;;
    risk*) optionARCH= ;;
    # Début ajout jeux instructions

    # Fin ajout jeux instructions
    *) optionARCH=-mcpu=cortex-m3;; #jeu d'instruction cortex-m3 par défaut
esac


${toolchain}gcc -c $optionARCH templatePy.c -o templatePy
