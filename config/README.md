# Archivos de configuración:

## Configuración general
Especifica el path al ejecutable de hashcat, las opciones de rendimiento y rutas a los directorios.

### host-config.json

En el campo paths se especificará la ruta a los directorios en los cuales estarán situados los diccionarios, reglas, máscaras y resultados. Se puede indicar una ruta tanto relativa como absoluta, por ejemplo: "wordlists" o "C:\\tools\\wordlists". En el caso de que no se quiera utilizar esta organización de directorios, habrá que indicar las rutas hasta los directorios en los que se encuentren los recursos necesarios.
```
{
	"executable": "hashcat64.exe",
	"resources": {
		"resource_level": "low",
		"resource_low": "--force",
		"resource_high": "-w 3"
	},
	"paths": {
		"wordlists_dir": "wordlists",
		"rules_dir": "rules",
		"masks_dir": "masks",
		"results_dir": "results"
	}
}
```

## Configuración personalizada de ataques secuenciales
Para ejecutar el programa autocrackeo, se tiene que proporcionar un archivo de configuración como parámetro de entrada 
```
--config config\test.json
```

* se pueden crear tantos archivos json como se quiera, pero se utilizará sólo uno por cada ejecución del programa. Ejemplos proporcionados:
	* test.json: ejemplo del que partir para crear archivos de configuración personalizados.
	* fast.json: configuración para una ejecución rápida con pocos intentos.
	* basic.json: configuración para una ejecución básica, que en minutos/horas sea capaz de probar las contraseñas/reglas/máscaras más frecuentes.
	* full.json: configuración para una ejecución más completa, puede tardar semanas, meses, años incluso. Además de probar las opciones básicas, añadirá reglas combinadas con diccionarios grandes, máscaras que abarquen más caracteres de fuerza bruta, etc.

## Parámetros
Se debe indicar la lista de archivos (diccionarios, reglas, máscaras) que se quieran utilizar.
```
"files": {
	"wordlists_files": [
		"custom.dic",
		"cracked.dic",
		"super.dic"
	],
	"rules_files": [
		"rules_fast.rule",
		"rules_basic.rule",
		"rules_full.rule"
	],
	"masks_files": [
		"masks_fast.hcmask",
		"masks_basic.hcmask",
		"masks_full.hcmask"
	]
}
```

## Ataques
Hashcat tiene varios modos de ataque (-a0 directo, -a1 combinado, -a3 fuerza bruta e híbridos -a6/-a7). Dependiendo del tipo de ataque que se quiera lanzar, hay que añadir unos recursos u otros, por lo que se ha dividido esta sección en varias partes para facilitar la definición de los mismos:

[] indica que puedes añadir todos los que desees
Los archivos: wordlist=w, rules=r y masks=m
Las introducciones manuales: rules_manual_left="j", rules_manual_right="k" y mask="m" 

| Tipos de ataque                    | Resumen de parámetros      | Ejemplo de password 
|------------------------------------|----------------------------|---------------------
| straight                           | [w]                        | word
| straight_with_rules_manual         | [w] + "j"                  | Word
| straight_with_rules_files          | [w] + [r]                  | Word
| straight_with_combined_rules_files | [w] + r + r                | .Word.
| combinator                         | w + w                      | wordtest
| combinator_with_rules_manual       | w + w + "j" + "k"          | .WordTest.
| brute_force_automatic              | -i min max                 | zzzzzzz
| brute_force_with_masks_manual      | "m" + -i min max           | zzzzzzz
| brute_force_with_masks_files       | m + -i min max             | zzzzzzz
| hybrid_right_with_masks_files      | w + m + "j" + -i min max   | Word999
| hybrid_right_with_masks_manual     | w + "m" + "j" + -i min max | Word999
| hybrid_left_with_masks_files       | w + m + "k" + -i min max   | 999Word
| hybrid_left_with_masks_manual      | w + "m" + "k" + -i min max | 999Word
|----------------------------------------------------------------------------------------
| one_word_per_hash                  | [w]                        | username 

Nota: En el ataque one_word_per_hash, sólo admite archivos de hash (hash_file) en dos formatos:
* hash
* username:hash añadiendo como argumento de entrada --extra-params "--username".
Este ataque sirve para probar usuario = contraseña. Hace falta un wordlist con todos los nombres de usuario con el mismo orden y número de líneas que el hasfile.

### Definición de los ataques
Para seleccionar archivos de diccionarios/reglas/máscaras en cada ataque hay varias formas:
Por ejemplo, teniendo definidos los siguientes diccionarios en los parámetros...
```
"wordlists_files": ["custom.dic", "cracked.dic", "super.dic", "*"]
```
1. **{"wordlists": [0,2]}**: ejecutará ese ataque utilizando los diccionarios de las posiciones 0 y 2 definidas en los parámetros ("custom.dic" y "super.dic").
2. **{"wordlists": [3]}**: ejecutará ese ataque con lo indicado en la posición 3 "\*", por lo que utilizará todos los archivos dentro del directorio wordlists/*
	* Esto puede resultar interesante si sueles utilizar un par de diccionarios, pero tienes muchísimos más de gran tamaño ("rockyou.txt", "hashkiller-dict.txt"...) a los cuales sólo les pasarías un ataque directo. La opción de añadir "\*" como diccionario te evita tener que escribir todos los diccionarios dentro de un directorio, y además se ejecutará de forma recursiva si está compuesto por más directorios.
3. **{"wordlists": []}**: ejecutará ese ataque con todos los diccionarios definidos anteriormente en los parámetros ("custom.dic", "cracked.dic", "super.dic" y "*").
	***¡CUIDADO!** Al unir las opciones de definir diccionarios con "\*" y listar los diccionarios para el ataque con [] en el mismo archivo de configuración, se duplicarán los mismos ataques ("custom.dic", "cracked.dic", "super.dic", "custom.dic", "cracked.dic", "super.dic", "más_diccionarios_del_directorio.dic", "...")

	* Lo mismo ocurre con máscaras y reglas
	* Para las reglas manuales, habrá que definir una en cada ataque entre comillas "c". Si quieres omitir la regla manual, pero ejecutar el ataque, añade la regla de no modificar nada ":".

Cada línea se corresponde con un ataque a ejecutar:
```
"attacks" : {
		"straight": [
			{"wordlists": []},
		],
		"straight_with_rules_manual": [
			{"wordlists": [], "rules": "l$1$8"},
			{"wordlists": [], "rules": "c$1$8"}
		],
		"straight_with_rules_files": [
			{"wordlists": [], "rules": [0]},
		],
		"straight_with_combined_rules_files": [
			{"wordlists": [], "rules": [0,0]}
		],
		"combinator": [
			{"wordlists": [0,0]},
			{"wordlists": [2,0]}
		],
		"combinator_with_rules_manual": [
			{"wordlists": [0,0], "rules_left": "c", "rules_right": "c$2$0$1$8"},
			{"wordlists": [2,0], "rules_left": ":", "rules_right": "c$2$0$1$8"}
		],
		"brute_force_automatic": [
			{"increment_enable": 0, "increment_min": 0, "increment_max": 0},
			{"increment_enable": 1, "increment_min": 1, "increment_max": 6}
		],
		"brute_force_with_masks_manual": [
			{"masks": "?u?1?1?1?1?d?d -1?l?s", "increment_enable": 0, "increment_min": 0, "increment_max": 0},
			{"masks": "?l?d?u", "increment_enable": 1, "increment_min": 1, "increment_max": 6}			
		],
		"brute_force_with_masks_files": [
			{"masks": [0], "increment_enable": 1, "increment_min": 1, "increment_max": 6}
		],
		"hybrid_right_with_masks_files": [
			{"wordlists": [], "rules_left": "c", "masks": [0], "increment_enable": 1, "increment_min": 1, "increment_max": 6}
		],
		"hybrid_right_with_masks_manual": [
			{"wordlists": [], "rules_left": "u", "masks": "20?d?d", "increment_enable": 1, "increment_min": 1, "increment_max": 4},
			{"wordlists": [], "rules_left": "c", "masks": "?d?d?d?d", "increment_enable": 1, "increment_min": 1, "increment_max": 4}
		],
		"hybrid_left_with_masks_files": [
			{"wordlists": [], "rules_right": "", "masks": [0], "increment_enable": 1, "increment_min": 1, "increment_max": 6}		
		],
		"hybrid_left_with_masks_manual": [
			{"wordlists": [], "rules_right": "u", "masks": "20?d?d", "increment_enable": 1, "increment_min": 1, "increment_max": 4},
			{"wordlists": [], "rules_right": "c", "masks": "?d?d?d?d", "increment_enable": 1, "increment_min": 1, "increment_max": 4}
		],
		"one_word_per_hash":[
			{"wordlists": [0]}
		]
	}
```

## Ejemplo:
* template.json es un archivo de configuración de ataques vacío para utilizarlo de plantilla cuando se quiera crear una nueva configuración personalizada.
* test.json es únicamente para ver un ejemplo de cada tipo, gran parte de los ataques están repetidos con opciones diferentes. Servirá como guía para construir un nuevo config.json personalizado.
* quick_test.json, fast.json, basic.json y full.json son algunos archivos preparados para utilizarse tal cual, dependiendo de la complejidad que se quiera.