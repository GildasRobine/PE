# Développement d'un simulateur de fautes sur des instructions en assembleur

Projet d'étude réalisé dans le cadre de notre 3ème année à l'École des Mines de Saint-Étienne. Ce programme permet d'afficher un code compilé en assembleur, de choisir une instruction à fauter et d'observer les fautes possibles.

Les modèles de fautes possibles sont bit-set, bit-reset et bit-flip. Le nombre de bits fautés doit être entre 1 et 32 bits contigus. Il est aussi possible d'insérer un masque manuellement. 


## Jeux d'instructions compatibles

* ARM
* AVR
* MIPS
* RISC V


## Premiers pas

Ces instructions vous permettront d'obtenir une copie du projet en cours d'exécution sur votre machine locale à des fins
 de développement et de test.

### Prérequis

Installation de Python3 (--version Python 3.6) :
```
sudo apt-get install python3.6
```
Installation des Toolchains :
* ARM : https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads
	* Une fois la toolchain installée, la rajouter au PATH : export PATH=$PATH:{install_dir}/gcc-arm-none-eabi-8-2018-q4-major-linux/bin
* AVR : 
```
sudo apt-get install gcc-avr binutils-avr avr-libc
sudo apt-get install gdb-avr
```
* MIPS (binutils-2.30, gcc-7.3.0, gdb-8.1): https://www.linux-mips.org/wiki/Toolchains
* RISC V : https://github.com/riscv/riscv-gnu-toolchain
	* Attention installation très longue

Installation de st-util : https://github.com/texane/stlink

## Lancer le test

```
cd simulateurInjection
./scriptShell.sh -arch=<jeu_instruction> -f=<fichier>
```
jeu_instruction : arm, avr, mips, risc
fichier : fichier .elf après compilation du programme
Exemple : 
 ```
 ./scriptShell.sh -arch=arm -f=project/build/test.elf
  ```

### Recherche des fautes possibles
Lors du lancement du programme, celui-ci affiche les instructions du fichier .elf :
```
 ...
 80002f6:	4c07      	ldr	r4, [pc, #28]	; (8000314 <main+0x30>)
 80002f8:	2201      	movs	r2, #1
 80002fa:	f44f 7100 	mov.w	r1, #512	; 0x200
 80002fe:	4620      	mov	r0, r4
 ...
 ```

Une fois le programme lancer, il va falloir choisir l'instruction à fauter et les caractéristiques de la faute :
* Choix de l'adresse de la faute en hexa (ex: 8000d42)
* Nombre de bits à fauter (entre 1 et 32)
* Type de faute à simuler (Bitset (s) - Bitreset (r) - Bitflip (f))
```
Veuillez séléctionner l'adresse de l'instruction à fauter : 80002f8
Combien de bits voulez-vous fauter (entre 1 et 32) : 1
Bitset (s) - Bitreset (r) - Bitflip (f)
Quel type de faute voulez-vous simuler : r
Simulation d'une attaque de type r sur 1 bits sur l'instruction : 
 80002f8:	2201      	movs	r2, #1
```

Le programme affiche alors les potentielles corruptions de l'instruction avec le modèle de fautes indiqué 
(opcode en hexa + correspondance assembleur).
  ```
   6:	2200      	movs	r2, #0
   8:	2001      	movs	r0, #1
   a:	0201      	lsls	r1, r0, #8
```
### Simulateur

Le simulateur ne fonctionne que pour la toolchain ARM et l'utilitaire st-util pour le moment. Pour que la simulation 
puisse fonctionner, il faut lancer st-util dans un autre terminal : 
```
st-util -m
```
L'ajout de l'option -m permet de ne pas avoir à relancer st-util à chaque fois qu'on quitte la simulation.


Une fois que le programme a affiché les corruptions possibles, l'utilisateur peut choisir de simuler une de ces
 possibilités en entrant l'adresse de la corruption (6, 8 ou a dans l'exemple précédent).

```
Voulez-vous corrompre l'instruction (oui/non) : oui
Par quelle instruction remplacer l'instruction : 6
```
Une fois la corruption sélectionée, va placer cette instruction dans une partie réservée de la mémoire. Pour ce faire,
il faut que votre projet contienne la fonction suivante dans le main.c :
```
void mem_reserved_corrupt(void)
{
//nop à remplacer :
asm("nop;");
}
```
Avec certains compilateurs, il faudra appeler au moins une fois la fonction dans votre main. En effet, lorsque la fonction
n'est jamais appelée, certains compilateurs suppriment l'instruction et cela risque de décaler les autres instructions.

Une fois la corruption choisie, le programme insère l'instruction dans le programme et le recompile.
```
void mem_reserved_corrupt(void)
{
asm(" add r0, r0;");
}
```

Une fois le projet compiler avec l'instruction corrompue, le programme lance GDB, se connecte au port 4242 (que vous avez 
connecté à la carte via st-util), charge le programme et initialise des points d'arrêt sur
l'instruction à corrompre et après l'instruction corrompue.
```
Reading symbols from blink32/build/blink32.elf...
Remote debugging using :4242
Reset_Handler () at startup_stm32f100xb.s:82
82	  movs r1, #0
Loading section .isr_vector, size 0x1d0 lma 0x8000000
Loading section .text, size 0xb98 lma 0x80001d0
Loading section .rodata, size 0x30 lma 0x8000d68
Loading section .init_array, size 0x4 lma 0x8000d98
Loading section .fini_array, size 0x4 lma 0x8000d9c
Loading section .data, size 0xc lma 0x8000da0
Start address 0x8000cac, load size 3500
Transfer rate: 4 KB/sec, 583 bytes/write.
Breakpoint 1 at 0x8000d42
Breakpoint 2 at 0x800029e: file Src/main.c, line 113.
(gdb) 
``` 
En plus de cela, le programme renvoie l'adresse de l'instruction corrompue et celle de l'instruction suivant l'instruction 
à corrompre :
``` 
Pour effectuer la corruption, entrer les commandes jump *0x800029c, jump *0x8000D44
``` 

Pour lancer le débogage, enter la commande "continue". Le programme fonctionne normalement. Lorsqu'il s'arrête sur le point
d'arrêt de l'instruction à corrompre, vous pouvez choisir de le faire fonctionner normalement avec la commande "continue"
ou de passer par l'instruction corrompue avec la commande "jump" :
```
(gdb) continue 
Continuing.

Breakpoint 1, 0x080002f8 in main () at Src/main.c:101
101			HAL_GPIO_WritePin(GPIOC, LD3_Pin, GPIO_PIN_SET);
(gdb) jump *0x800029c
Line 113 is not in `main'.  Jump anyway? (y or n) y
Continuing at 0x800029c.

Breakpoint 2, 0x0800029e in mem_reserved_corrupt () at Src/main.c:113
113	asm(" movs r2, #0;");}
(gdb) jump *0x80002FA
Line 101 is not in `mem_reserved_corrupt'.  Jump anyway? (y or n) y
Continuing at 0x80002fa.

Breakpoint 1, 0x080002f8 in main () at Src/main.c:101
101			HAL_GPIO_WritePin(GPIOC, LD3_Pin, GPIO_PIN_SET);
(gdb) 

```
Sur cet exemple, nous avons effectué la première itération de notre boucle avec l'instruction de base, puis nous avons
utilisé l'instruction corrompue dans la seconde itération.

Une fois que vous avez fini avec le débogueur, quittez le simplement avec la commande "quit". Le programme se réinitialisera.

### Comment utiliser un projet personnel

Le simulateur est fourni avec un projet test "blink32". Afin d'utiliser le simulateur avec votre propre projet, il faut respecter ces quelques règles :
* Mettre son dossier projet dans le dossier "simulateurInjection" (avec le script bash et les scipts python)
* Votre dossier project dois être consitué : 
    * d'un dossier "Src" avec le main.c
    * d'un dossier "build" où on retrouve le fichier compilé .elf
    * d'un makefile à la racine de votre projet
    * Un exemple est donnée avec le programme (blink32)
* Dans simulationCorruption.sh modifier les variables "nomDossier" et "nomFichierCompile"
* Ajouter la fonction "mem_reserved_corrupt" dans votre main.c

## Problèmes connus


* Pour Cortex-M3 et RISC-V : si lors d'un bitset sur une instruction 16 bits les quatre derniers bits passent à 1 alors 
l'instruction passe sur 32 bits et elle va prendre comme 2ème moitié d'instruction la suivante.
	* Exemple : ddf0 suivit d'un nop (bf00) va donner fdf0 bf00 (ldc2l	15, cr11, [r0]) après le dernier bitset
* S'il y a une erreur lors de la configuration de gcc du type : Building GCC requires GMP 4.2+, MPFR 2.3.1+ and MPC 0.8.0+, 
il faut se placer dans le dossier de gcc et effectuer cette commande : ./contrib/download_prerequisites


## Auteurs

* Antoine Boré 
* Gildas Robine

## Encadrants

* Jean-Max Dutertre
* Pierre-Alain Moëllic
* Olivier Potin




