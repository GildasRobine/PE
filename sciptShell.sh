#!/bin/bash


echo "Consequence d'une modification de bits sur une instruction"
echo "Utilisation : modificationBytes.sh <fichier .elf>"
echo nom du script : $0

arm-none-eabi-objdump -d $1

#On demande à l'utilisateur d'indiquer l'adresse de l'instruction à fauter
echo 

echo -n "Veuillez séléctionner l'adresse de l'instruction à fauter : "
read add_inst

#On stocke la ligne correspondant à l'instruction que l'on veut fauter
arm-none-eabi-objdump -d $1 | egrep -w $add_inst: >> instruction.txt


while :; do
  read -p "Combien de bits voulez-vous fauter (entre 1 et 16) : " nb_fault_bits
  [[ $nb_fault_bits =~ ^[0-9]+$ ]] || { echo "Entrer un nombre valide"; continue; }
  if ((nb_fault_bits > 0 && nb_fault_bits <= 16)); then
    break
  else
    echo "le nombre n'est pas entre 1 et 16"
  fi
done

var=s
while :; do
	echo "Bitset (s) - Bitreset (r) - Bitflip (f)"
  read -p "Quel type de faute voulez-vous simuler : " faultType
  if [ "s" == "$faultType"  -o  "r" == "$faultType"  -o  "f" == "$faultType" ]
	then
		echo "ok"
    break
  else
    echo "L'entrée ne correspond pas aux fautes proposées"
  fi
done


#On récupere l'index de la derniere instruction fautée
index=$(python3 setbit.py $nb_fault_bits $faultType)

#On affiche les instructions fautée
arm-none-eabi-objdump --start-address=6 --stop-address=$index -d hexToArm.elf
rm instruction.txt

exit 0
