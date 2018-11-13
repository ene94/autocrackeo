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

# En proceso
* simplificar la obtención de resultados: mostrar en pantalla sólo comando del hashcat + crackeados al instante, generar archivos con el nombre del hashlist y contenido usuario:contraseña en un directorio concreto al usar -r o --results
* posibilidad de saltarse la secuencia de ataques y pasar directamente a los resultados con las teclas "Ctrl+c"
* se ha movido la definición de los directorios base de cada archivo de configuración de ataques, al archivo de configuración general host-conf.json
* comprobaciones de existencia de ficheros necesarios

# TODO
* omitir la salida en pantalla del hashcat y simplificarla al máximo. Ideas:
	* simple barra de progreso
	* notificación de hashes crackeados
* generar un informe analizando los resultados (por cada comando o en total). Ideas:
	* contraseñas crackeadas/desconocidas
	* tiempo de ejecución
	* patrones encontrados...
* añadir funcionalidad de guardar y restaurar sessiones
* añadir más diccionarios interesantes:
	* hashkiller.txt
	* default.txt