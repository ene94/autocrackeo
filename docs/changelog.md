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

# En proceso
* Añadir búsqueda rápida de tipos de hash, para introducir "ntlm" en lugar de "1000", por ejemplo.
* Hacer más amigable el uso de diferentes formatos de hashes

# TODO
* comprobaciones de existencia de ficheros...
* report.json: generar un informe con los resultados básicos de la ejecución
* añadir opción para ordenar la ejecución de los ataques
* omitir la salida en pantalla del hashcat y simplificarla al máximo. Ideas:
	* simple barra de progreso
	* notificación de hashes crackeados
* generar un informe analizando los resultados (por cada comando o en total). Ideas:
	* contraseñas crackeadas/desconocidas
	* tiempo de ejecución
	* patrones encontrados...
* añadir funcionalidad de guardar y restaurar sessiones

# Para mejorar
* analizar la efectividad de los comandos enviados al hashcat y optimizar el uso de los mismos
* generar archivos de diccionarios, reglas, máscaras que optimicen el funcionamiento
	* diccionarios representativos
	* reglas/máscaras especializadas para diferentes tipos de ataque
	* reglas generadas tras el análisis de las contraseñas que se van crackeando
	* máscaras que engloben varias reglas y se ejecuten en un tiempo adecuado
	* añadir archivos conocidos como:
		* best64.rule
		* d3ad0ne.rule
		* T0XIC.rule
		* rockyou.txt
		* hashkiller.txt
		* default.txt