# Archivos con resultados

## Para uso interno
* potfile.pot: No tocar este archivo durante la ejecución del hashcat. Lo utiliza para llevar la cuenta de los hashes ya crackeados y así evitar volver a trabajar en ellos, para mostrar otros resultados...

## Para mostrar/guardar resultados
* utilizar como argumento de entrada `--just-results` o `-r`
	* se guardará con el nombre del [hashlist].res a los ficheros con formato hash:password, o user:hash:password si se utiliza el parámetro -e="--username" y el tipo de hash lo permite.