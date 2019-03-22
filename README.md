# Développement d'un simulateur de fautes sur des instruction en assembleur

Projet d'étude réalisé dans le cadre de notre 3ème année à l'École des Mines de Saint-Étienne. Ce programme permet d'afficher un code compiler en assembleur, de choisir une instruction à fauter et d'observer les fautes possibles.

Les modèles de fautes posibles sont bit-set, bit-reset et bit-flip. Le nombre de bits fautés doit être entre 1 et 32 bits contigus. Il est aussi possible d'insérer un masque manuellement. 


## Jeux d'instructions compatibles

* ARM
* AVR
* MIPS
* RISK V


## Premiers pas

Ces instructions vous permettront d'obtenir une copie du projet en cours d'exécution sur votre machine locale à des fins de développement et de test.

### Prérequis

Installation de Python3 (--version Python 3.6) :
```
sudo apt-get install python3.6
```
Installation des Toolchains :
* ARM :
* AVR : 
```
sudo apt-get install gcc-avr binutils-avr avr-libc
sudo apt-get install gdb-avr
```
* MIPS (binutils-2.30, gcc-7.3.0, gdb-8.1): https://www.linux-mips.org/wiki/Toolchains
* RISK V :

## Lancer le test

```
cd simulateurInjection
./scriptShell.sh <jeu_instruction> <fichier>
```
jeu_instruction : arm, avr, mips, risk

fichier : fichier .elf après compilation du programme

Une fois le programme lancer, il va falloir choisir l'instructionà fauter et les caractéristiques de la faute :
* Choix de l'adresse de la faute en hexa (ex: 12c)
* Nombre de bits à fauter (entre 1 et 32)
* Type de faute à simuler (Bitset (s) - Bitreset (r) - Bitflip (f))

Le programme affiche alors les potentiels corruptions de l'instruction avec le modèle de fautes indiqué (opcode en hexa + correspondance assembleur).


## Problèmes connus

### ARM Cortex-M3

* Si lors d'un bitset sur une instruction 16 bits les quatres derniers bits passent à 1 alors l'instruction passe sur 32 bits et elle va prendre comme 2ème moitié d'instruction la suivante.
	* Exemple : ddf0 suivit d'un nop (bf00) va donner fdf0 bf00 (ldc2l	15, cr11, [r0]) après le dernier bitset
* S'il y a une erreur lors de la configuration de gcc du type : Building GCC requires GMP 4.2+, MPFR 2.3.1+ and MPC 0.8.0+, il faut se placer dans le dossier de gcc et effectuer cette commande : ./contrib/download_prerequisites


## Auteurs

* Antoine Boré 
* Gildas Robine

## Encadrants

* Jean-Max Dutertre
* Pierre-Alain Moellic
* Olivier Potin




