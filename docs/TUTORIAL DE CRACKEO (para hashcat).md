# TUTORIAL DE CRACKEO (con hashcat)

## Cosas que preparar para cada proyecto:
Generar diccionario personalizado: wordlist_custom.txt
* nombres de la empresa
* dominios y subdominios
* palabras clave
* nombres de usuario sacadas de los hashes
* política de contraseñas → caracteres mínimos, mayúsculas, minúsculas, números, signos de puntuación...


## Tipos de hashes (con ejemplos para identificarlos rápidamente): -m
https://hashcat.net/wiki/doku.php?id=example_hashes

* 0 = MD5 --> 16 bytes ~ 32 caracteres
	* 8743b52063cd84097a65d1633f5c74f5

* 100 = SHA1 --> 20 bytes
	* b89eaac7e61417341b710b727768294d0e6a277b

* 500 = md5crypt, MD5 (Unix), Cisco-IOS $1$ (MD5)
	* $1$28772684$iEwNOgGugqO9.bIz5sk8k/

* 900 = MD4
	* afe04867ec7a3845145579a95f72eca7

* 1000 = NTLM ~ 32 cacateres
	* user:permission:lmhash:nthash:::
	* b4b9b02e6f09a9bd760f388b67351e2b

* 1100 = Domain Cached Credentials (DCC), MS Cache
	* user:hash:domain:organization?::: --> para que hascat lo reconozca formatear a hash:user
	* 4dd8965d1d476fa0d026722989a6b772:3060147285011

* 1800 = sha512crypt , SHA512 (Unix)
	* $6$52450745$k5ka2p8bFuSmoVT1tzOyyuaREkkKBcCNqoDKzYiJL9RaE8yMnPgh2XzzF0NDrUhgrcLwg78xs1w5pJiypEdFX/

* 2100 = Domain Cached Credentials 2 (DCC2), MS Cache 2
	* $DCC2$10240#user#hash --> para que hascat lo reconozca formatear a hash:user
	* $DCC2$10240#tom#e4e938d12fe5974dc42a90120bd9c90f

* 3000 = LM → max length = 14 (las parte de 7 en 7)
	* user:permission:lmhash:nthash:::
	* 299bd128c1101fd6

* 3100 = Oracle H: Type (Oracle 7+), DES(Oracle) 
	* --> para que hashcat lo reconozca formatear a hash:user
	* 7A963A529D2E3229:3682427524

* 5500 = NetNTLMv1, NetNTLMv1+ESS
	* u4-netntlm::kNS:338d08f8e26de93300000000000000000000000000000000:9526fb8c23a90751cdd619b6cea564742e1e4bf33006ba41:cb8086049ec4736c

* 5600 = NetNTLMv2
	* admin::N46iSNekpT:08ca45b7d7ea58ee:88dcbe4446168966a153a0064958dac6:5c7830315c7830310000000000000b45c67103d07d7b95acd12ffa11230e0000000052920b85f78d013c31cdb3b92f5d765c783030

* 13400 = KeePass 1 (AES/Twofish) and KeePass 2 (AES)
	* $keepass$*1*50000*0*3757...


## Tipos de ataque con hashcat: -a
* 0 = Straight → (word)
* 1 = Combination → (wordword)    
* 3 = Brute-force → mask (?u?l?l?l?l?l?d?d)
* 6 = Hybrid: → dict + mask (word11)
* 7 = Hybrid: → mask + dict (11word)


### Straight: -a 0
Prueba cada línea del diccionario

```
hashcat64.exe -m 0 -a 0 C:\hashes.txt C:\wordlist1.txt
con reglas desde archivo: hashcat64.exe -m 0 -a 0 C:\hashes.txt C:\wordlist1.txt -r C:\rules1.rule
con reglas a mano: hashcat64.exe -m 0 -a 0 C:\hashes.txt C:\wordlist1.txt -j 'c$2$0$1$8'
varios diccionarios: hashcat64.exe -m 0 -a 0 C:\hashes.txt C:\wordlist1.txt C:\wordlist2.txt -r C:\rules1.rule
```

--> Nota: cuidado en windows con "$", hay que hacer con '$'

### Combination: -a 1
Prueba cada combinación de parejas de palabras de dos wordlists

```
hashcat64.exe -m 0 -a 1 C:\hashes.txt C:\wordlist1.txt C:\wordlist2.txt
combinando reglas: hashcat64.exe -m 0 -a 1 C:\hashes.txt C:\wordlist1.txt C:\wordlist2.txt -j 'c' -k 'c$2$0$1$8'
```

### Brute-force: -a 3
Prueba todas las combinaciones posibles

```hashcat64.exe -m 0 -a 3 C:\hashes.txt
con máscara: hashcat64.exe -m 0 -a 3 C:\hashes.txt ?u?l?l?l?l?l?d?d?d?d
```

Probar fuerza bruta hasta 0-9 caracteres, tardaría años...
Hay que pasarle máscaras con patrones conocidos para poder probar contraseñas de más caracteres sin tanto coste de tiempo.
```
hashcat64.exe -m 0 -a 3 C:\hashes.txt ?u?l?l?l?l?l2018
hashcat64.exe -m 0 -a 3 C:\hashes.txt ?u?u?u?u -i --increment-min 1 --increment-max 4
```


### Hybrid: -a 6 (wordlist + mask)
Prueba la combinación de las líneas del wordlist concatenado con una máscara a la derecha
```
hashcat64.exe -m 0 -a 6 C:\hashes.txt C:\wordlist1.txt ?d?d
con reglas: hashcat64.exe -m 0 -a 6 C:\hashes.txt C:\wordlist1.txt ?d?d -j "c$1"
increment: hashcat64.exe -m 0 -a 6 .\hashes.txt .\wordlist.txt ?d?d?d?d?d -i --increment-min 1 --increment-max 5
```


### Hybrid: -a 7 (mask + wordlist)
Prueba la combinación de las líneas del wordlist concatenado con una máscara a la izquierda 

```
hashcat64.exe -m 0 -a 7 C:\hashes.txt ?d?d C:\wordlist1.txt
con reglas: hashcat64.exe -m 0 -a 7 C:\hashes.txt ?d?d C:\wordlist1.txt -k "c$1"
con increment: hashcat64.exe -m 0 -a 7 .\hashes.txt ?d?d?d?d?d .\wordlist.txt -i --increment-min 1 --increment-max 5
```


## Máscaras: ?1 -1 ?l?u?d?s -i --increment-min --increment-max
Se pueden utilizar máscaras en los modos de ataque a=3,6,7
Se puede especificar cuántos y qué tipos de caracteres va a probar hascat para fuerza bruta:

Built-in charsets:
* ?l = abcdefghijklmnopqrstuvwxyz
* ?u = ABCDEFGHIJKLMNOPQRSTUVWXYZ
* ?d = 0123456789
* ?h = 0123456789abcdef
* ?H = 0123456789ABCDEF
* ?s = ``«space»!"#$%&'()*+,-./:;<=>?@[]^_`{|}~``
* ?a = ?l?u?d?s
* ?b = 0x00 - 0xff

Custom charsets:
* built in: ?1?2?3?3?3?4?4 -1 .+_ -2?u -3?l -4?d
* manual: ?1?1?1?1?1 -1 .+-!1234abcdABCD
* de un fichero: -1 charsets/special/Russian/ru_ISO-8859-5-special.hcchr
* si falla por carácteres raros: --hex-charset
* por defecto: 
	* -1/--custom-charset1	?l?d?u
	* -2/--custom-charset2	?l?d
	* -3/--custom-charset3	?l?d\*!$@_
	* -4/--custom-charset4	NULL

Modo incremental: puedes abarcar de golpe casos como 0-9, 00-99, 000-999 y 0000-9999.
Se puede utilizar la opción incremental, para que comience a probar fuerza bruta desde x caracteres y acabe cuando llegue a y caracteres: --increment/-i --increment-min/--increment-max.
Si pones una máscara de tamaño 10 (?1?1?1?1?1?1?1?1?1?1 -1?d -i --increment-min 1 --imcrement-min 3), prevalece el increment y hará desde 0 hasta 999, por mucho que la máscara abarque más casos.
* --increment o -i: activa el modo incremental
* --increment-min 1: emepzar por 1 caracter
* --increment-max 4: parar en 4 caracteres

Cargar máscaras de un fichero: 
* escribir máscaras en un fichero línea a línea con formato: charset1,charset2,charset3,charset4,mask

Se pueden personalizar los patrones de fuerza bruta, por ejemplo indicando que cierta posición sea números y signos de puntuación definidos, cierta otra posición sea sólo minúsculas, otra posición sólo mayúscula, etc.
De esta forma, se consiguen eliminar muchísimos intentos que no son necesarios y que nos hacen perder tiempo.
```
hashcat64.exe -m 0 -a 3 C:\hashes.txt ?d?d?d?d
hashcat64.exe -m 0 -a 3 C:\hashes.txt ?a?a?a?a?a?a?a?a
hashcat64.exe -m 0 -a 3 C:\hashes.txt ?u?l?l?l?l?l?d?d
hashcat64.exe -m 0 -a 3 C:\hashes.txt ?1?2?2?2?2?2?3?3 -1?u -2?l -3?d.!
hashcat64.exe -m 0 -a 3 C:\hashes.txt 20?d?
hashcat64.exe -m 0 -a 3 C:\hashes.txt ?u?u?u?u -i --increment-min 1 --increment-max 4
hashcat64.exe -m 0 -a 3 C:\hashes.txt C:\masks.hcmask
hashcat64.exe -m 0 -a 3 C:\hashes.txt -i ?1?1?1?1?1?1?1?1?1 --increment --increment-min 8 -1?l?d-@!
```

## Diccionarios:
* Se le puede pasar un archivo: wordlist.txt
* Varios archivos en los casos de -a 0,1,6,7: wordlist.txt wordlist2.txt
	* El caso -a 1 sólo acepta 2 archivos de wordlists, ni más ni menos.
* O también un directorio que contenga archivos de texto y/o más directorios: wordlists/*
	--> en este caso se cogerían todos los archivos recursivamente
```
hashcat64.exe -m 0 -a 0 C:\hashes.txt C:\wordlist.txt
hashcat64.exe -m 0 -a 0 C:\hashes.txt C:\wordlist1.txt C:\wordlist2.txt
hashcat64.exe -m 0 -a 0 C:\hashes.txt C:\wordlists/\*
```

## Reglas: -r -j -k
https://hashcat.net/wiki/doku.php?id=rule_based_attack
* We pueden aplicar reglas a los modos de ataque a=0,1,6,7

Algunos archivos de reglas ya vienen creadas en hashcat:
* Kali: /usr/share/hashcat/rules
* Servidor de Crackeo: hashcat-3.6.0\rules

Mostrar (y no crackear) cada contraseña que probará al aplicar las modificaciones de las reglas al wordlist:
```
hashcat64.exe -m 0 -a 0 C:\hashes.txt C:\wordlist.txt -r C:\rule1.rule --stdout
```

Generar un fichero con las reglas que han tenido éxito: sólo funciona con -a 0
```
hashcat64.exe -m 0 -a 0 C:\hashes.txt C:\wordlist.txt -r C:\rule1.rule --debug-mode=1 --debug-file=matched.rule
```

Algunas reglas útiles definidas en hashcat:
* : no hacer nada
* l minúsculas
* u mayúsculas
* c primera mayúsculas, lo demás minúsculas
* C la primera minúsculas, lo demás mayúsculas
* t invierte las mayúsculas/minúsculas de toda la contraseña
* t1 toogle la mayúscula/minúscula de la posición 1 en concreto
* r invierte el orden
* $1 añade un 1 al final
* ^1 añade un 1 al principio
* sXY reemplaza los carácteres X por Y
* @X elimina todos los carácteres X
* E toda la frase en minúsculas, pone mayúsculas la primera letra de la frase, y cada letra después de un espacio
* eX lo mismo pero después de cada carácter X
* xNM Extrae M caracteres emepzando por la posición N

Ejemplos:
En wordlist.txt tendríamos el diccionario de palabras (por ejemplo: password)
En rule1.rule tendríamos las reglas, una por línea.
* u --> PASSWORD
* l --> password
* c --> Password
* C --> pASSWORD
* ^1 --> 1password
* $1 --> password1
* $1$7 --> password17
* ^7^1 --> 17password (¡ojo al orden!)
* c^.$s$1$7 --> .passwords17

Se pueden insertar varios archivos de reglas y se ejecutarán en orden todas las combinaciones:
wordlist.txt (password), rule1.rule (^1$1) y rule2.rule (^2$2)
```hashcat64.exe --stdout wordlist.txt -r rule1.rule -r rule2.rule
21password
2password1
1password2
password12
```

En los modos de ataque -a 1,6,7 se divide en lado derecho e izquierdo, por lo que al escribir la regla hay que indicar a cuál de ellos aplicarlo. En el caso de wordlist1 wordlist2 -j se aplicará al wordlist1, y las reglas de -k al wordlist2.
```
hashcat64.exe -m 0 -a 0 C:\hashes.txt C:\wordlist.txt -r C:\rule1.rule
hashcat64.exe -m 0 -a 1 C:\hashes.txt C:\wordlist1.txt C:\wordlist2.txt -j "c" -k "c$2$0$1$8"
hashcat64.exe -m 0 -a 6 C:\hashes.txt C:\wordlist.txt ?d?d -j "c$1"
hashcat64.exe -m 0 -a 7 ?d?d C:\hashes.txt C:\wordlist.txt -k "c$1"
```


## Resultados: --potfile-path --show --left --username -o --outfile-format
Generar resultados:
* --potfile-path: Ruta en la que se quieren guardar las contraseñas que crackee. Antes de empezar lee el potfile para descargar de la lista de hashes las que ya se hayan crackeado (para no repetirse)
* -o outfile.txt: Almacenar contraseñas guardadas en un archivo, en un formato concreto (indepediente de hashcat)
* --outfile-format: almacenarlo en un formato concreto:
	* 1: hash
	* 2: contraseña en claro
	* 3: hash:claro
	* 4: contraseña en hexadecimal
	* 5: hash:hex
	* 6: plain:hex
	* 7: hash:plain:hex

Mostrar resultados:
* --show: Mostrar contraseñas YA crackeadas en formato hash:plain
* --left: Mostrar hashes NO crackeados
* --username: Mostrar contraseñas crackeadas en claro y con usuario (para los hashes que llevan el campo del usuario)
```
hashcat64.exe -m 0 -a 3 C:\hashes.txt --potfile-path C:\potfile.pot
hashcat64.exe -m 0 -a 3 C:\hashes.txt --potfile-path C:\hpotfile.pot --show
hashcat64.exe -m 0 -a 3 C:\hashes.txt --potfile-path C:\hpotfile.pot --left
hashcat64.exe -m 0 -a 3 C:\hashes.txt --potfile-path C:\hpotfile.pot --show --username
hashcat64.exe -m 0 -a 3 C:\hashes.txt -o cracked.txt --outfile-format 2
```

## Restauración: --session --restore --restore-file-path
Cuando llevas horas ejecutando un comando de hashcat y tienes que pararlo por lo que sea, pero quieres luego seguir con ello sin volver a empezar, puedes utilizar estas opciones:
* --session SessionName: para darle nombre a una sesión, y que se vaya guardando su progreso
* --restore: para indicar que se quiere restaurar desde el último checkpoint guardado
* --restore-file-path: especificar una ruta diferente para lamacenar el punto de restauración
* Por defecto, si sales del hashcat con 'c' guarda el progreso en un archivo de restauración: hashcat_dir/hashcat.restore
* Si sales con 'q' o 'Ctrl+c' no guarda el progreso
```
hashcat64.exe -m 0 -a 3 C:\hashes.txt --session SessionName
hashcat64.exe -m 0 -a 3 C:\hashes.txt  --session SessionName --restore-file-path C:\SessionName.restore
hashcat64.exe --session SessionName --restore
```

# EXTRA: 

## Empty passwords:
aad3b435b51404eeaad3b435b51404ee (LM)
31d6cfe0d16ae931b73c59d7e0c089c0 (NTLM)

## Algo de john the ripper:

--show
--wordlist=wordlist.txt / -w=wordlist.txt
--pot=john.pot
--format=lm, nt, RAW-MD5, mscash, mscash2, netntlmv1, netntlmv2, oracle

Nota: si no sabes qué tipo de hash es viendo el formato, ejecutas el john sin la opción --format, y él intuirá cuál puede ser y te dará una lista de los posibles tipos de hash. Después vas probando cada uno de ellos en hashcat hasta que lo reconoce. Por defecto john acepta muchísimos formatos y los interpreta como quiere/puede, en cambio hashcat o se lo pasas como debe ser o no lo admite. Para no perder el tiempo, comprobar con hashcat que has reconocido bien el formato, porque john podría pasarse horas crackeando con un formato incorrecto y sin sacar nada.

## Otros recursos: 
greps para extraer contraseñas: 
https://www.unix-ninja.com/p/A_cheat-sheet_for_password_crackers

Para formatear de crackmap output a las contraseñas en claro: (dependiendo del formato)
```
awk '{if (NR!=1) {print $5}}' pass.txt | grep -x '.\{1,30\}' | sort | uniq > pass2.txt
awk '{if (NR!=1) {print $2}}' pass.txt | grep -x '.\{1,30\}' | sort | uniq > pass2.txt
```