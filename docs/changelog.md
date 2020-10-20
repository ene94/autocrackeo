
# Cambios

* 06/06/2018:
	* compatibilidad windows/linux

* 16/08/2018:
	* cambiar la entrada de parámetros del teclado al script con opción de ayuda
	* reestructurar el proyecto para poder ampliar el alcance del mismo
		* Archivos de configuración de la ejecución: separar toda la configuración modificable por el usuario en un único archivo JSON
		* Autocrackeo.py: script principal que interpreta la configuración y llama a los métodos de ataque definidos
		* Clase Attack: parsea los datos de ataque y llama a los correspondientes métodos de la clase hashcat
		* Clase Hashcat: específica de hashcat y sus parámetros para facilitar las llamadas a la herramienta
	* crear varios modos de funcionamiento en base a la configuración (json): rápido, básico, completo...
	* analizar, mostrar y almacenar los resultados:
		* outfile=plaintext_passwords.txt: contraseñas en texto plano crackeadas en la ejecución
		* out_file_cracked=hashes_cracked.txt: user:password crackeados
		* out_file_left=hashes_left.txt: user:hash sin crackear
	* añadir opción de ataque one_word_per_hash --> ¿hashlist[i] == hash(wordlist[i])? (línea a línea)

* 25/09/2018:
	* añadir archivos conocidos de hashes, reglas, máscaras y diccionarios.
	* cambiar el orden de los ataques pasando la fuerza bruta al último lugar. En realidad depende del orden en el que se escriba el archivo de configuración.
	* mover la configuración de entorno (executable,resources) a un único fichero "host-config.json", fuera de los config.json.
	* mover la opción de añadir parámetros extra del hashcat como argumentos de entrada --extra-params="--username" o -e="--username", en lugar de en los archivos config.json.
	* actualizar los archivos de ejemplos de configuración y READMEs acorde a los cambios.
	* Añadir búsqueda rápida de tipos de hash, para introducir "NTLM" en lugar de "1000", por ejemplo.

* 06/02/2019: v1.3
	* simplificar la obtención de resultados: mostrar en pantalla sólo comando del hashcat + crackeados al instante, generar archivos con el nombre del hashlist y contenido usuario:contraseña en un directorio concreto al usar -r o --results
	* posibilidad de saltarse la secuencia de ataques y pasar directamente a los resultados con las teclas "Ctrl+c"
	* se ha movido la definición de los directorios base de cada archivo de configuración de ataques, al archivo de configuración general host-conf.json
	* comprobaciones de existencia de ficheros necesarios
	* eliminar posibilidad de elegir ruta a cada directorios, identifica la ruta del archivo de configuración con el parámetro -c, y utiliza como directorio base el directorio anterior.
	* arreglado para que funcione también en windows, que te obliga a ejecutarlo desde el directorio del hashcat.
	* se han añadido las configuraciones all_wordlists_all_rules.json, lm.json y ntlm_from_lm.json
	* ejecutar en bucle un mismo ataque para varios archivos y tipos desde un archivo json con una lista de hash_file, hash_type y extra_params.
	* eliminar innecesario texto con resultados.
	* añadir elección de ruta a /results/ donde dejar el potfile y los resultados de la ejecución
	* cambiar argumento -c para utilizar ruta relativa desde /autocrackeo/config/ con -c test.json o ruta absoluta C:\test\test.json
	* añadir argumento de entrada para elegir el path del archivo custom.dic a utilizar

* 08/02/2019: v1.4
	* añadir pathwell.hcmask mask to all_wordlists_all_rules.json
	* opción -c "all" para que ejecute en secuencialmente cada archivo de configuración definido en el archivo all.json

* 08/02/2019: v1.5
	* cambios en las configuraciones para ajustar los tiempos de ejecución
	* añadidos recursos y ataques del repositorio kaonashi de github

* 07/03/2020: v1.6
	* cambios en el formato de mostrar comentarios por pantalla y colores
	* añadida la opción --feedback  para volcar contraseñas nuevas del potfile al diccionario personalizado (-w)

* 05/04/2020: 1.7
	* pequeños arreglos
	* actualización del script para descargar los recursos externos: setup.py
	* añadido el archivo requirements.txt

* 25/04/2020: v1.8
	* añadida interfaz gráfica con tkinter para lanzar el comando de autocrackeo en un thread aparte
	* añadida la función de logger para guardar en un archivo los comandos que se han ido ejecutando
	* update readme with demo images

* 08/05/2020: v1.9
	* arreglar rutas de autocrackeo si se lanza desde otro directorio
	* quitar del usuario la parte de escribir el .json de los ataques
	* si no incluyes un wordlist con la opción -w, por defecto usa como diccionario primario wordlists\super.dic
	* cambiar nomenclatura de configuración -c por ataque -a, que es menos confuso
	* recuperar contenido original de super.dic que había borrado sin querer
	* gui: en lugar de recalcular el comando y ejecutar, que lea el contenido del text box por si el usuario lo cambmia a mano


# PARA SUBIR V2 

* 02/07/2020: v2.0
	* Añadir recursos corporate masks del repositorio github.com/golem445/Corporate_Masks. Unirlas en un archivo de ataques corporate_masks.json y añadirlo al all.json.
	* Si pulsas 3 veces seguidas en menos de 1 segundo de diferencia Ctrl+c en lugar de saltarse un ataque, para la ejecución de autocrackeo y acaba

# EN PROCESO
* XX/07/2020: v2.0
* acabar setup.py con la parte de descomprimir diccionarios y comprobar que funcione tanto en linux como en windows

# TODO

* GUI: añadir desplegable de ataques (quick_test, fast, basic, custom...)
* separar máscaras de kaonashi entre el basic, full y bruteforce forever
* NTDS analisys
* check how to combine --feedback and --loopback
* search hash from pattern
* add john the ripper for múltiple hybrid attack like ?a?a?w?a?a
* work with machine readable results to update a progress bar
* list of slow/fast hashes to skip some "long/hard" attacks
* more exception handling
* arreglar: Skipping invalid or unsupported rule in file D:\projects\MaiShadow\autocrackeo\rules\OneRuleToRuleThemAll.rule on line 8210: ^o^─à^─é^o^t
