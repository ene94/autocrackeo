# Autocrackeo
Programa en python que automatiza el uso del hashcat para crackear contraseñas

La idea es tener varios archivos fast.json, basic.json, full.json, etc. con ataques de hashcat predefinidos que se ajusten a la velocidad/eficiencia que se requiera en cada momento. Al ejecutar el autocrackeo especificando uno de estos archivos, el programa ejecutará secuencialmente (sin necesidad de supervisión) los ataques de hashcat con los diccionarios, reglas y máscaras definidos en él.

> python3 autocrackeo.py -m 1000 -i docs\test_files\ntlm.hash  -w docs\test_files\custom.dic -o docs\test_files\results --feedback -a all --verbose

Nueva GUI para generar y ejecutar el comando de forma más visual: `python3 autocrackeo-gui.py`
![Autocrackeo GUI](docs/autocrackeo-gui.PNG)

Ejecución de autocrackeo:
![Autocrackeo](docs/autocrackeo.PNG)

Archivos de resultados generados:
![Resultados](docs/results.PNG)

## Requisitos
Probado en windows/linux con python 3
* [python3](https://www.python.org/downloads/)
* [hashcat](https://github.com/hashcat/hashcat)
	* Hay que tener en cuenta que dependiendo de la versión del hashcat (en windows y a partir de la 3.6) te fuerza a lanzar el hashcat únicamente desde su propio directorio.

## Configuración inicial

Instalar módulos requeridos:
```
pip3 install -r requirements.txt
```

Descargar recursos externos:
* Ejecutar el script de configuración donde están los enlaces a recursos externos que son muy interesantes (diccionarios, reglas, máscaras...)
```
python3 setup.py
```

## Manual de usuario

### Por dónde empezar...
Especifica el path al ejecutable de hashcat y las opciones de rendimiento en el archivo de configuración del equipo "src\HOST_CONFIG.json", por ejemplo:
* executable: hashcat64.exe (Windows) y hashcat (Linux) (en linux o  versiones anteriores de hashcat en windows puedes especificar la ruta absoluta)
* resources: Opciones de hashcat para funcionar dependiendo del equipo en el que se ejecuta: -D 1 -w 3 --force ...

Ejecuta el programa: 
* El programa muestra por pantalla la ejecución del hashcat, por lo que se puede interactuar con él:
	* **s**: mostrar estado (status) / también sirve el "Enter"
	* **p**: pausar (pause)
	* **r**: reanudar (resume)
	* **b**: saltarse fases de un mismo ataque (bypass)
	* **q**: saltarse un ataque completo (quit)
* Ctrl+C para cancelar todos los ataques  sobre un archivo de hashes


### Personalización
1. Modifica el archivo de configuración src\HOST-CONFIG.json para tu entorno y necesidades.
2. Introduce más archivos de diccionarios, reglas y máscaras en los directorios wordlists/, rules/ y masks/ respectivamente.
3. Modifica los archivos de configuración de ataques a tu gusto.
	* Lista los archivos de diccionarios, reglas y máscaras que quieras utilizar en este caso.
	* Define los modos ataque que quieras lanzar con sus parámetros correspondientes.

Nota: El tiempo que tarde en realizar un archivo de ataques dependerá de muchos factores como el número de hashes, el tipo de hash, el tamaño de los diccionarios, de las máscaras, la capacidad del equipo, etc.

### Ayuda
Para ver todas las opciones:
```python
python3 autocrackeo.py -h
```

### Ejemplos
Ejemplo más sencillo: lanza comandos de hashcat sobre el archivo de hashes de entrada  
Tenéis unos archivos de prueba en la siguiente ruta autocrackeo\docs\test_files: ntlm.hash y custom.dic
```console
python3 %PATH_AUTOCRACKEO%/autocrackeo.py -i %PATH_PROYECTO%\ntlm.hash -m 1000 -a all
```

Un archivo: pasando un diccionario de entrada personalizado y diciéndole donde dejar los resultados
```console
python3 %PATH_AUTOCRACKEO%/autocrackeo.py -m 1000 -i %PATH_PROYECTO%\ntlm.hash -w %PATH_PROYECTO%\custom_wordlist.dic -o %PATH_PROYECTO%\results_dir -e="--username" -a quick_test.json
```

Varios archivos secuencialmente: para más información ver explicación en la carpeta "docs/Ejemplos"
```console
python3 %PATH_AUTOCRACKEO%/autocrackeo.py -I %PATH_PROYECTO%\hash_files_list.json -w %PATH_PROYECTO%\custom_wordlist.dic -o %PATH_PROYECTO%\results -e="--username" -a quick_test.json 
```

Nota: en algunas versiones de hashcat te fuerza a ejecutar el hashcat desde el propio directorio del ejecutable, así que modificar las rutas a los archivos para ese caso concreto. Por ejemplo:
```console
cd \tools\hashes\hashcat-5.1.0\
python3 %PATH_AUTOCRACKEO%\autocrackeo.py -m ntlm  -i %PATH_PROYECTO%\ntlm.hash  -w %PATH_PROYECTO%\custom_wordlist.dic -o %PATH_PROYECTO%\results -a quick_test.json
```

Se recomienda el uso de las siguientes opciones:
* --feedback: cogerá las contraseñas del potfile y las volcará si no existen aún al archivo de diccionario personalizado (-w)
* --verbose: para ver más información sobre los comandos de hashcat que se van ejecutando uno tras otro
* -e="--username": si el archivo de hashes está con el formato "usuario:hash" se puede añadir la oopción "--username" en hashcat para que los resultados del potfile salgan con formato "usuario:contraseña" en lugar de únicamente la "contraseña".


## Recomendaciones de uso

### Recursos de proyecto

Se recomienda tener bajo un mismo directorio todos los recursos específicos de un mismo proyecto.

Hashes:
* almacenar todos los archivos con hashes que se recopilen para ese proyecto

Diccionarios:
* Diccionarios con palabras/frases específicas del proyecto (datos de cliente, servicios, usuarios...)


### Recursos de autocrackeo
Los enlaces a todos ellos para descargarlos de una vez se encuentran en el archivo setup.py:

Diccionarios: wordlists/
* cracked.dic: añadir aquí las contraseñas que vayas crackeando en cada proyecto para que te sirvan para los posteriores
* super.dic: recolección de palabras genéricas, lugares, colores, nombres, fechas... susceptibles de aparecer en contraseñas
* añadir más diccionarios:
	* rockyou: http://downloads.skullsecurity.org/passwords/rockyou.txt.bz2
	* hashkiller: https://hashkiller.co.uk/downloads.aspx
	* colecciones de usuarios, contraseñas, urls, patrones...: https://github.com/danielmiessler/SecLists
	* palabras típicas: https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt

Reglas: rules/
* fast.rule, basic.rule, full.rule: creadas específicamente para esta herramienta según en nivel de complejidad deseado
* añadir más reglas:
	* best64.rule, d3ad0ne.rule y T0XIC.rule: https://github.com/hashcat/hashcat/tree/master/rules
	* hob064.rule: https://github.com/praetorian-inc/Hob0Rules
	* OneRuleToRuleThemAll.rule: https://github.com/NotSoSecure/password_cracking_rules
	* toggles-lm-ntlm.rule: https://github.com/trustedsec/hate_crack/blob/master/rules/toggles-lm-ntlm.rule
	* haku34K.rule: https://raw.githubusercontent.com/kaonashi-passwords/Kaonashi/master/rules/haku34K.rule,
	* kamaji34K.rule: https://raw.githubusercontent.com/kaonashi-passwords/Kaonashi/master/rules/kamaji34K.rule,
	* yubaba64.rule: https://raw.githubusercontent.com/kaonashi-passwords/Kaonashi/master/rules/yubaba64.rule
		

Máscaras: masks/
* fast_hybrid.hcmask, basic.hcmask, basic_hybrid.hcmask, full.hcmask, full_hybrid.hcmask: creadas específicamente para esta herramienta según en nivel de complejidad deseado
* añadir más máscaras:
	* 2015-Top40-Time-Sort.hcmask: https://blog.netspi.com/netspis-top-password-masks-for-2015/
	* pathwell.hcmask: https://github.com/trustedsec/hate_crack/blob/master/masks/pathwell.hcmask
	* kaonashi.hcmask: https://raw.githubusercontent.com/kaonashi-passwords/Kaonashi/master/masks/kaonashi.hcmask"
	* rockyou-1-60.hcmask: https://raw.githubusercontent.com/hashcat/hashcat/master/masks/rockyou-1-60.hcmask


Configuraciones de ataques automáticos:
* quick_test.json, fast.json, basic.json, full.json: ataques predefinidos de menos a más complejidad
	* quick_test.json: prueba una vez los diccionarios custom, cracked y super
	* fast.json: configuración para una ejecución rápida con pocos intentos.
	* basic.json: configuración para una ejecución básica, que en minutos/horas sea capaz de probar las contraseñas/reglas/máscaras más frecuentes.
	* full.json: configuración para una ejecución más completa, puede tardar semanas, meses, años incluso. Además de probar las opciones básicas, añadirá reglas combinadas con diccionarios grandes, máscaras que abarquen más caracteres de fuerza bruta, etc.
* all_wordlists_all_rules.json: todas las combinaciones de cada diccionario con cada regla
* one_word_per_hash.json: generar un diccionario sólo con los nombres de usuario y probar únicamente usuario=contraseña
	* puede resultar útil teniendo hashes de formato de hashes complejos (que tardan mucho en cada prueba)
	* el número de líneas del hashlist y wordlist deben coincidir
* lm.json: prueba todas las combinaciones posibles de hashes en formato LM (1-8 caracteres)
* ntlm_from_lm.json: partiendo de un wordlist con contraseñas sacadas en LM (case insensitive) prueba todas las combinaciones de mayúsculas y minúsculas para sacar las contraseñas NTLM (case sensitive)


## Organización
El proyecto está dividido por directorios de distintos recursos. Aunque en ningún momento se restringe completamente a seguir esta estructura. Los directorios de hashes, diccionarios, reglas, máscaras y resultados, se pueden especificar como parámetros de entrada o en la configuración json, por lo que se pueden modificar o unificar perfectamente.

* En el directorio **wordlists/** se almacenaran los diccionarios que contengan palabras o frases susceptibles a aparecer en contraseñas.
* En el directorio **rules/** se almacenaran los archivos con reglas (modificaciones sobre las palabras del diccionario)
* En el directorio **masks/** se almacenaran los archivos con máscaras (patrones de fuerza bruta)
* En el directorio **config/** se almacenarán los archivos json que contienen la configuración y los ataques a ejecutar...
* En el directorio **src/** está el código fuente del programa.
* En el directorio **docs/** se almacenarán archivos de interés relacionados con el proyecto
	* changelog.md: aquí se irán indicando los cambios realizados y las nuevas ideas por desarrollar
	* Tutorial de crackeo (para hashcat).md: aquí he reunido los conceptos y ejemplos del hashcat que me han sido de utilidad para realizar este proyecto.
	* Archivo de hashes y diccionario para pruebas.

## Autora
* **Eneritz Azqueta** → Auditora en **S21sec**