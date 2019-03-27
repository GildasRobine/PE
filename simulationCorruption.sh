#!/bin/bash

####################################################################################################
##################                      START USER                                ##################
####################################################################################################


nomDossier=blink32
nomFichierCompile=blink32

####################################################################################################
##################                       END USER                                 ##################
####################################################################################################


echo "Consequence d'une modification de bits sur une instruction"
echo "Utilisation : scriptShell.sh <fichier .elf>"
echo "nom du script : $0"
echo
rm instruction.txt 2> /dev/null 
nbparam=0
printHelp="
Pour lancer le script : ./scriptShell.sh -arch=<nom_arch> -f=<nom_fichier.elf>\n
-arch,	Sélection du jeu d'instructions (arm, avr, mips, risc)\n
-f,	Sélection du fichier elf à fauter\n
"
archOK=false
fichierOK=false
#Lecture des paramètres en entrée
for param in "$@"
do	
	case $param in
	#Si le paramètre commence par -arch, on vient choisir le jeu d'instruction
	-arch*)
		archOK=true
	# Début ajout jeux instructions
		case $param in
		*arm)
		instructionSet=arm-none-eabi-;;
		*avr)
		instructionSet=avr-;;
		*mips)
		instructionSet=mipsel-unknown-linux-gnu-;;
		*risc)
		 instructionSet=riscv64-unknown-linux-gnu-;;
	# Fin ajout jeux instructions
		*) instructionSet=arm-none-eabi-;; #jeu d'instruction arm par défaut
		esac;;
	#Si le paramètre commence par -f, on vient choisir le fichier contenant les instructions
	-f*) 	nomFichier=${param:3}
	#On verfie l'existence du fichier
		if [ -f $nomFichier ]
		then
			fichierOK=true
		else
			echo "Le fichier $nomFichier n'existe pas"
		fi;;
	*) 	echo ;;
	esac
done
#Vérification des argmuments obligatoire
if ( $archOK && $fichierOK ); then
	echo "Jeu d'instruction : $instructionSet"
	echo "Nom du fichier $nomFichier"
else
	echo -e $printHelp
	exit
fi

#On affiche les instructions asm du programme à attaquer
#Le second argument correspond au fichier contenant le code
${instructionSet}objdump -d $nomFichier

timestamp(){
	date +%y-%m-%d_%T_%3N
}


####################################################################################################
##################                    PREMIERE PARTIE                             ##################
####################################################################################################

echo

while :; do
 
	#On demande à l'utilisateur d'indiquer l'adresse de l'instruction à fauter
	read -p "Veuillez séléctionner l'adresse de l'instruction à fauter : " add_inst
	#On stocke la ligne correspondant à l'instruction que l'on veut fauter dans un fichier texte lu par python
	${instructionSet}objdump -d $nomFichier | egrep -w $add_inst: >> instruction.txt
	# On verifie que le fichier existe et est non vide
	if [ -s "instruction.txt" ]
	then
		
		break
	else
		echo "Rentrez une adresse d'instruction valide" 
	fi
done
#On demande à l'utilisateur d'indiquer le nombre de bits à fauter
while :; do
  read -p "Combien de bits voulez-vous fauter : " nbFaultBits
	#On vérifie que le nombre indiqué est bien un entier positif
  [[ $nbFaultBits =~ ^[0-9]+$ ]] || { echo "Entrer un nombre valide"; continue; }
  #On vérifie que le nombre indiqué est entre 1 et 32
  if ((nbFaultBits > 0 && nbFaultBits <= 32)); then
		#Lorsqu'une entrée est valide, on sort de la boucle infinie
    break
  else
    echo "le nombre n'est pas entre 1 et 32"
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

# On recupère la date et l'heure pour nommer le fichier de log
timeS=$(timestamp)
# On créer le fichier de log et on remplie l'en-tête
echo "Simulation d'une attaque de type $faultType sur $nbFaultBits bits sur l'instruction : " | tee log/$timeS.log
cat instruction.txt | tee -a log/$timeS.log
#On récupere l'index de la derniere instruction fautée
ret=$(python3 createFault.py $nbFaultBits $faultType $instructionSet)


set -- $ret

for retPy in "$@"
do
    case $retPy in
    0x*)
        index=$retPy;;
    16to32:*)
        echo "Une faute entraine un passage de 16 à 32 bits : ${retPy:7}XXXX";;

    32to16:*)
        echo "Une faute entraine un passage de 32 à 16 bits : ${retPy:7:6} et ${retPy:13} ";;
    *);;
    esac
done
#On affiche les instructions fautées et on les stocks dans le fichier de log créer plus haut

mkdir -p log
${instructionSet}objdump --start-address=6 --stop-address=$index -d toObjdump.elf | tee -a log/$timeS.log


####################################################################################################
##################                    DEUXIEME PARTIE                             ##################
####################################################################################################


#  /!\ La simulation de l'instruction corrompue ne fonctionne qu'avec ARM pour le moment /!\
echo "La simulation ne fonctionne qu'avec l'architecture ARM pour le moment"
read -p "Voulez-vous corrompre l'instruction (oui/non) : "  corrupt
case $corrupt in
	o*)
	while :; do
	    # On demande à l'utilisateur l'adresse de la faute qu'il souhaite simuler
		read -p "Par quelle instruction remplacer l'instruction : " ligneInstr
		${instructionSet}objdump --start-address=6 --stop-address=$index -d toObjdump.elf | egrep -w $ligneInstr: >> instructionModif.txt
		if [ -s "instructionModif.txt" ]
		then
			
			break
		else
			echo "Rentrez une adresse d'instruction valide" 
		fi
	done
	arm-none-eabi-objdump -d "$nomDossier"/build/"$nomFichierCompile".elf | egrep "mem_reserved_corrupt" >> addrFct.txt
	
	#Script python qui crée un main avec l'instruction corrompue dans une zone mémoire
	breakpoint=$(python3 corruptSimu.py)

	#On récupère les adresses de l'instruction corrompue et de l'instruction à corrompre
	set -- $breakpoint
	breakInit=$1
	breakFault=$(printf "0x%X\n" $(($2+0x2)))
	jumpInit=$(printf "0x%X\n" $(($1+0x2)))
	jumpFault=$2
	#On compile avec un main.c contenant l'instruction corrompue
	cd ${nomDossier}
	make &> /dev/null 
	cd ..
	echo -e "\nPour effectuer la corruption, entrer les commandes jump *$jumpFault, jump *$jumpInit\n\n"

	pathgdb=
	arm-none-eabi-gdb -q "$nomDossier"/build/"$nomFichierCompile".elf -ex="target remote :4242" -ex="load" -ex="break *$breakInit" -ex="break *$breakFault"
	echo "Réinitialisation des fichiers"
	#Remplace le fichier avec l'instruction corrompue par le fichier de base
	rm "$nomDossier"/Src/main.c
	mv "$nomDossier"/Src/buffer.c "$nomDossier"/Src/main.c
	cd "$nomDossier"/
	#Recompile avec le fichier de base
	make clean  &> /dev/null
	make  &> /dev/null
	cd ..
	;;
	n*);;
	*);;
esac


rm instruction.txt 2> /dev/null
rm instructionModif.txt 2> /dev/null 
rm addrFct.txt 2> /dev/null 


#Si le programme s'est bien passé, on sort avec le code 0
exit 0
