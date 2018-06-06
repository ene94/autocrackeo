# -*- coding: utf-8 -*-

# Datos necesarios

# MODIFICAR dependiendo de dónde se ejecute

# Ejecutable:
hashcat = "hashcat64.exe" # windows
#hashcat = "hashcat " # linux

#Opciones de rendimiento:
options = " --force " # local
#options = " -w 3 " # servidor de crackeo

# CONSTANTES

header = '''

--------------------------------------------------------------------------------

   _____          __         _________                       __                 
  /  _  \  __ ___/  |_  ____ \_   ___ \____________    ____ |  | __ ____  ____  
 /  /_\  \|  |  \   __\/  _ \/    \  \/\_  __ \__  \ _/ ___\|  |/ // __ \/  _ \ 
/    |    \  |  /|  | (  <_>      \____|  | \// __ \\  \___|    <\  ___(  <_> 
\____|__  /____/ |__|  \____/ \______  /|__|  (____  /\___  >__|_ \\___  >____/ 
        \/                           \/            \/     \/     \/    \/       

                                                     
--------------------------------------------------------------------------------
'''
hashes_dir = "hashes"
results_dir = "results"

wordlist_custom = " wordlist_custom.txt "# palabras claves del cliente, nombres de sus usuarios... -->  crear para cada proyecto
wordlist_crackeados = " wordlist_crackeados.txt "# contraseñas crackeadas de otros proyectos
wordlist_variado = " wordlist_super.txt "# de todo un poco: fechas, lugares, nombres y apellidos, palabras sueltas...
rules_super = " rules_super.rule "# archivo de reglas
increment_min = " 1 "# increment min/max
increment_max = " 7 "

potfile = " " + results_dir + "hashcat.pot "# dónde guardar las contraseñas que se crackeen
debug = " --debug-mode=1 --debug-file=" + os.path.join(results_dir, "successful_rules.txt ") # sólo funciona en -a 0

# Valores por defecto si no introduces nada por teclado
hashes_file = "test.hash"
hash_format = "1000"

# Mostrar datos y descripción
description = '''
Este script está pensado para funcionar con:
	* 3 archivos de diccionarios: wordlist_super.txt, wordlist_crackeados.txt y wordlist_custom.txt
	* 1 archivo de reglas: rule_super.txt

Introduce palabras clave del proyecto en wordlist_custom.txt

Si algo falla será cosa de la configuración, adáptalo a tu entorno en el archivo config.py.
'''

format_description = '''
Para los siguientes hashes escribir lo que aparece a continuación: MD5, LM, NTLM, NTLMv1, NTLMv2, DCC, DCC2, ORACLE H.
Para cualquier otro tipo de hash escribir el número correspondiente en hashcat (por ejemplo, si fuese un MD4 introducir 900)
Más información sobre los tipos de hashes:  https://hashcat.net/wiki/doku.php?id=example_hashes
'''

format_dictionary = {'MD5': '0', 'SHA1': '100', 'LM': '3000', 'NTLM': '1000', 'NTLMv1': '5500', 'NTLMv2': '5600', 'DCC': '1100', 'Unix': '1800', 'DCC2': '2100', 'ORACLE H': '3100', 'KEEPASS': '13400'}

user_guide = '''
Puedes interactuar con el hashcat de la siguiente manera: 
	's' ver el estado 
	'p' pausar la ejecución 
	'r' reanudar la ejecución  
	'b' saltarse esa prueba (por ejemplo uno de los diccionarios con los que ejecuta un comando, o uno de los tamaños de máscara del --increment) 
	'q' saltarte el comando completo (sin guardar progreso)
	'c' saltarte el comando completo guardando el progreso (para ser posteriormente restaurado)
	'Ctrl + c' salir del todo")
'''