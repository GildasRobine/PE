#!/bin/bash


echo "Consequence d'une modification de bits sur une instruction"
echo "Utilisation : scriptShell.sh <fichier .elf>"
echo nom du script : $0

#On affiche les instructions asm du programme à attaquer
arm-none-eabi-objdump -d $1

timestamp(){
	date +%y-%m-%d_%T_%3N
}



echo

while :; do
 
	#On demande à l'utilisateur d'indiquer l'adresse de l'instruction à fauter
	read -p "Veuillez séléctionner l'adresse de l'instruction à fauter : " add_inst
	#On stocke la ligne correspondant à l'instruction que l'on veut fauter
	arm-none-eabi-objdump -d $1 | egrep -w $add_inst: >> instruction.txt
	if [ -s "instruction.txt" ]
	then
		
		break
	else
		echo "Rentrez une adresse d'instruction valide" 
	fi
done
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


timeS=$(timestamp)
echo "Simulation d'une attaque de type $faultType sur $nbFaultBits bits sur l'instruction : " | tee log/$timeS.txt
cat instruction.txt | tee -a log/$timeS.txt
#On récupere l'index de la derniere instruction fautée
index=$(python3 setbit.py $nbFaultBits $faultType)
#On affiche les instructions fautée


mkdir -p log
arm-none-eabi-objdump --start-address=6 --stop-address=$index -d hexToArm.elf | tee -a log/$timeS.txt
rm instruction.txt

#Si le programme s'est bien passé, on sort avec le code 0
exit 0
