# Autocrackeo
Script en python que automatiza el uso del hashcat para crackear contraseñas


## Prerequisitos
* python3 o superior
* [hashcat](https://github.com/hashcat/hashcat)

## Manual de usuario
1. Introduce archivos con hashes en /hashes
2. Rellena con palabras clave del proyecto el wordlist_custom.txt
3. Ejecuta el script: `python3 autocrackeo.py`
4. Introduce el nombre del archivo de hashes (por ejemplo test.hash)
5. Introduce el tipo de hash (por ejemplo NTLM o 1000)
6. Introduce el nombre del diccionario personalizado (por ejemplo wordlist_custom.txt)
7. Asegúrate de leer en pantalla cómo interactuar con el hashcat, y ¡que comience el crackeo!

* En el directorio **/hashes** se almacenaran los archivos de texto que contengan hases.
	* test.hash: con los hashes ntlm de las contraseñas (test, Password1, admin2018, .nombre_apellido.)

* En el mismo directorio que el script autocrackeo.py se almacenarán los **diccionarios**.
	* wordlist_crackeados.txt: contraseñas crackeadas en proyectos anteriores.
	* wordlist_super.txt: palabras comunes, nombres, apellidos, lugares, fechas...
	* wordlist_custom.txt: palabras clave del proyecto actual a modificar. 

* En el directorio **/results** irán apareciendo los hashes crackeados, entre otras cosas.
	* hashcat.pot: archivo para que hashcat reconozca los hashes que ya ha crackeado.
	* cracked.txt: archivo donde aparecerán las contraseñas averiguadas en texto plano. --> todo
	* successful_rules.txt: archivo que indicará las reglas que han funcionado

NOTA 1: El tiempo que tarde dependerá de muchos factores como el número de hashes, el tipo de hash, el tamaño de los diccionarios, la capacidad del equipo, etc.

NOTA 2: Los comandos que se ejecutan también tienen gran impacto en la efectividad y la duración de la ejecución, por lo que se irán optimizando poco a poco.


## Compatibilidad
Probado en windows con python 3 o superior


## Autora
* **Eneritz Azqueta** → proyecto realizado como becaria de Auditoría en **S21sec**