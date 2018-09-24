# Formato
Hashcat admite muchísimos tipos de hashes. Cada tipo tiene su formato concreto, aunque hashcat admite introducir la mayoría de sus hashes como user:hash o simplemente una lista de hashes. Por ejemplo, serían igual de válidos para un hash NTLM:
* user:hash --> formato que admite hashcat con el parámetro adicional --username
* user:permission:lm_hash:nt_hash::: --> formato original de ntlm (lo mismo para otros tipos)
* hash --> únicamente el hash

# Contraseñas de prueba
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