#!/bin/sh


# Exemples de programmation du shell.
# Pour plus d'informations, lire la page de manuel de bash (76 pages !).


echo "Consequence d'une modification de bits sur une instruction"
echo "Utilisation : modificationBytes.sh <fichier .elf>"
echo nom du script : $0

arm-none-eabi-objdump -d $1

echo "\n\n"
echo -n "Veuillez séléctionner l'adresse de l'instruction à fauter : "
read add_inst

arm-none-eabi-objdump -d $1 | egrep -w $add_inst: >> instruction.txt
index=$(python3 setbit.py)

arm-none-eabi-objdump --start-address=6 --stop-address=$index -d hexToArm.elf
rm instruction.txt

exit 0
