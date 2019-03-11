#!/bin/bash


echo "Consequence d'une modification de bits sur une instruction"
echo "Utilisation : scriptShell.sh <fichier .elf>"
echo nom du script : $0

#On affiche les instructions asm du programme à attaquer
arm-none-eabi-objdump -d $1

timestamp(){
	date +%y%m%d_%H%M%S_%3N
}



echo 
#On demande à l'utilisateur d'indiquer l'adresse de l'instruction à fauter
echo -n "Veuillez séléctionner l'adresse de l'instruction à fauter : "
read add_inst

#On stocke la ligne correspondant à l'instruction que l'on veut fauter
arm-none-eabi-objdump -d $1 | egrep -w $add_inst: >> instruction.txt

#On demande à l'utilisateur d'indiquer le nombre de bits à fauter
while :; do
  read -p "Combien de bits voulez-vous fauter (entre 1 et 16) : " nbFaultBits
	#On vérifie que le nombre indiqué est bien un entier positif
  [[ $nbFaultBits =~ ^[0-9]+$ ]] || { echo "Entrer un nombre valide"; continue; }
  #On vérifie que le nombre indiqué est entre 1 et 16
  if ((nbFaultBits > 0 && nbFaultBits <= 16)); then
		#Lorsqu'une entrée est valide, on sort de la boucle infinie
    break
  else
    echo "le nombre n'est pas entre 1 et 16"
  fi
done

#On demande à l'utilisateur d'indiquer le type de faute à simuler
while :; do
	echo "Bitset (s) - Bitreset (r) - Bitflip (f)"
  read -p "Quel type de faute voulez-vous simuler : " faultType
  #On vérifie que l'entrée correspond à une des attaques proposées
  if [ "s" == "$faultType"  -o  "r" == "$faultType"  -o  "f" == "$faultType" ]
	then
		#Lorsqu'une entrée est valide, on sort de la boucle infinie
    break
  else
    echo "L'entrée ne correspond pas aux fautes proposées"
  fi
done

echo "Simulation d'une attaque de type $faultType sur $nbFaultBits bits"
#On récupere l'index de la derniere instruction fautée
index=$(python3 setbit.py $nb_fault_bits $faultType)
#On affiche les instructions fautée
timeS=$(timestamp)
mkdir -p log
arm-none-eabi-objdump --start-address=6 --stop-address=$index -d hexToArm.elf >> log/$timeS.txt
rm instruction.txt

#Si le programme s'est bien passé, on sort avec le code 0
exit 0
