
# COMANDOS DE EJEMPLO 

--> ir variando: -c con los valores "quick_test.json", "fast.json", "basic.json", "full.json", "all_wordlists_all_rules.json" o "all"

## desde el directorio del proyecto
```
python3 %PATH_AUTOCRACKEO%\autocrackeo.py -i hashes\ntlm.hash -m 1000 -o results -e="--username" -w custom.dic -c quick_test.json
```

## desde directorio de hashcat
```
python3 %PATH_AUTOCRACKEO%\autocrackeo.py -i %PATH_PROYECTO%\hashes\ntlm.hash -m 1000 -c quick_test.json -w %PATH_PROYECTO%\custom_wordlist.dic -o %PATH_PROYECTO%\results -e="--username"
```

## Realimentar el custom.dic con las contraseñas crackeadas del potfile.pot
* UPDATE: esto ya se ha implementado al script con la opción: --feedback
```
cd D:\CLIENTES\2019\Proyecto\
cat results/potfile.pot | awk -F: '{print $NF}' >> custom.dic && sort custom.dic | uniq > custom.dic2 && mv custom.dic2 custom.dic
```


---

# Todos los archivos de configuración: -c all

Al ejecutar el programa dejar la opción de configuración como "all":
```
-c all
```

/autocrackeo/config/all:
```
{
	"config_files": [
		"quick_test.json",
		"fast.json",
		"basic.json",
		"all_wordlists_all_rules.json",
		"full.json"
	]
}
```

# Todos los archivos de hashes: -F hash_files_list.json

Al ejecutar el programa especificar el archivo json con la lista de hashes y sus parámetros:
```
-I C:\Users\eazqueta\Desktop\crackeo\hash_files_list.json
```

Y crear un archivo con los detalles: (por ejemplo: hash_files_list.json)
```
{
	"list": [
		{
			"hash_file": "C:\\Users\\eazqueta\\Desktop\\crackeo\\lm-ntlm.hash",
			"hash_type": "LM",
			"extra_params": "--username"
		},
		{
			"hash_file": "C:\\Users\\eazqueta\\Desktop\\crackeo\\lm-ntlm.hash",
			"hash_type": "NTLM",
			"extra_params": "--username"
		},
		{
			"hash_file": "C:\\Users\\eazqueta\\Desktop\\crackeo\\md5.hash",
			"hash_type": "md5",
			"extra_params": ""
		}
	]
}
```

# Repetir ataques sólo de diccionario custom:
sin repetir super.dic ni cracked.dic, ni rockyou.dic...
```
-c all_custom.json -w custom.dic
-c all_custom_insane.json -w custom.dic
```