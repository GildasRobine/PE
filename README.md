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

## Auteurs

* Antoine Boré 
* Gildas Robine

## Encadrants

* Jean-Max Dutertre
* Pierre-Alain Moellic
* Olivier Potin



