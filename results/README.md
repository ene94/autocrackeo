# Archivos con resultados

## Para uso interno
* plaintext_password.txt: No se debe modificar el archivo durante la ejecución del programa. Se utiliza para poder notificar los hashes nuevos que se van crackeando tras cada ataque. También almacena la lista de contraseñas en texto claro.
* potfile.pot: No tocar este archivo durante la ejecución del hashcat. Lo utiliza para llevar la cuenta de los hashes ya crackeados y así evitar volver a trabajar en ellos, para mostrar otros resultados...

## Para mostrar/guardar resultados
* utilizar como argumento de entrada `--just-results`
	* hashes_cracked.txt: se llama a la opción --show de hashcat y se vuelca el resultado a este archivo con la lista de hashes crackeados.
	* hashes_left.txt: se llama a la opción --left de hashcat y se vuelca el resultado a este archivo con la lista de hashes sin crackear aún.