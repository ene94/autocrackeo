# Autocrackeo
Script en python que automatiza el uso del hashcat para crackear contraseñas


## Requisitos
* Versión python3.6
* [hashcat](https://github.com/hashcat/hashcat)

## Manual de usuario

### Por dónde empezar

1. Especifica el path al ejecutable de hashcat en el archivo de configuración, por ejemplo:
	"executable": "hashcat64.exe" --> en windows
	"executable": "hashcat" --> en linux
2. Prueba cualquiera de los comandos del apartado *Ejemplos* de más abajo

### Personalización

1. Introduce archivos con hashes en el directorio hashes.
2. Introduce archivos de diccionarios, reglas y máscaras en los directorios wordlists, rules y masks respectivamente.
3. Modifica el archivo de configuración config.json para tu entorno y necesidades.
	* **Presta atención al valor del ejecutable y de la opción de recursos**.
	* Lista los archivos de diccionarios, reglas y máscaras que quieras utilizar en este caso.
	* Define los modos ataque que quieras lanzar con sus parámetros correspondientes.
		* La idea es tener varios archivos config.json (fast.json, basic.json, full.json...) que se ajusten a la velocidad/eficiencia que se requiera en cada momento.
		* En config\test.json hay múltiples ejemplos del formato requerido en cada tipo de ataque.
4. Ejecuta el programa: `python3 autocrackeo.py -m 1000 hashes\test.hash --config config\fast.json`
Durante la ejecución...
	* En plaintext_passwords.txt se irán almacenando las contraseñas en texto planon.
	* Se muestra por pantalla la ejecución del hashcat, por lo que se puede interactuar con él:
		* **s**: mostrar estado (status)
		* **p**: pausar (pause)
		* **r**: reanudar (resume)
		* **b**: saltarse fases de un mismo ataque (bypass)
		* **q**: saltarse un ataque completo (quit)

Nota: El tiempo que tarde dependerá de muchos factores como el número de hashes, el tipo de hash, el tamaño de los diccionarios, la capacidad del equipo, etc.

### Ayuda
Para ver todas las opciones: `python3 autocrackeo.py -h`

	usage: autocrackeo.py [-h] -m HASH_TYPE --config CONFIG_FILE [--just-results]
	                      [--version]
	                      hash_file

	Automated Hashcat usage tool

	positional arguments:
	  hash_file             path to the file with hashes to crack

	optional arguments:
	  -h, --help            show this help message and exit
	  -m HASH_TYPE          hashcat's hash type number, more info here:
	                        https://hashcat.net/wiki/doku.php?id=example_hashes
	  --config CONFIG_FILE  configuration json file to use with specific attacks
	  --just-results        skips the attacks and just shows the results using the
	                        potfile
	  --version             show program's version number and exit

### Ejemplos
```
python3 autocrackeo.py -m 1000 hashes\test.hash --config config\quick_test.json
python3 autocrackeo.py -m 1000 hashes\test.hash --config config\fast.json
python3 autocrackeo.py -m 1000 hashes\test.hash --config config\basic.json
python3 autocrackeo.py -m 1000 hashes\test.hash --config config\full.json
python3 autocrackeo.py -m 1000 hashes\test_only_hash_format.hash --config config\one_word_per_hash.json
python3 autocrackeo.py -m 1000 hashes\test_user_hash_format.hash --config config\test.json
python3 autocrackeo.py -m 1000 hashes\test.hash --config config\fast.json --just-results
```

## Organización
El proyecto está dividido por directorios de distintos recursos. Aunque en ningún momento se restringe completamente a seguir esta estructura. Los directorios de hashes, diccionarios, reglas, máscaras y resultados, se pueden especificar como parámetros de entrada o en la configuración json, por lo que se pueden modificar o unificar perfectamente.

* En el directorio **hashes/** se almacenaran los archivos de texto que contengan hases.
* En el directorio **wordlists/** se almacenaran los diccionarios que contengan palabras o frases susceptibles a aparecer en contraseñas.
* En el directorio **rules/** se almacenaran los archivos con reglas.
* En el directorio **masks/** se almacenaran los archivos con máscaras.
* En el directorio **results/** se almacenarán ciertos archivos utilizados por hashcat e irán apareciendo los hashes crackeados, entre otros.
* En el directorio **config/** se almacenarán los archivos en formato json que contienen la configuración de opciones de rendimiento, lista de archivos de diccionario/reglas/máscaras a utilizar, ataques a ejecutar...
* En el directorio **src/** está el código fuente del programa.
* En el directorio **docs/** se almacenarán archivos de interés relacionados con el proyecto:
	* changelog.md: aquí se irán indicando los cambios realizados y las nuevas ideas
	* Tutorial de crackeo (para hashcat).md: aquí he reunido los conceptos y ejemplos del hashcat que me han sido de utilidad para realizar este proyecto.

## Compatibilidad
Probado en windows/linux con python 3.6.3

## Autora
* **Eneritz Azqueta** → proyecto realizado como becaria de Auditoría en **S21sec**