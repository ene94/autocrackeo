# Formato

Hashcat admite muchísimos tipos de hashes. Cada tipo tiene su formato concreto, aunque hashcat admite introducir la mayoría de sus hashes como user:hash o simplemente una lista de hashes. Por ejemplo, serían igual de válidos para un hash NTLM:
* user:hash --> formato que admite hashcat con el parámetro adicional --username (recomendado)
* user:permission:lm_hash:nt_hash::: --> formato original de ntlm
* hash

## Mi recomendación para esta herramienta
1. Convendría hacer una prueba con el hash en el formato original, de forma que se haya identificado correctamente el tipo de hash a utilizar.
2. Entre simplemente "hash" o "user:hash" yo utilizaría la segunda opción, ya que al mostrar los resultados, se generará un archivo "hashes_cracked.txt" en el cual aparecerá la relación de credenciales usuario-contraseña que puede resultar útil, en lugar de una simple lista de contraseñas en claro.


# Hashes de prueba

* test
* Password1
* admin2018
* ClayJensen1
* Azul2018
* .nombre_apellido
* contraseña24
* donostia1357
* VACACIONES321
* JMa8fvPu
* Username1
* username123