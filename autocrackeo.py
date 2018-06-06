# -*- coding: utf-8 -*-
import os
import sys

# ESTILO
class bcolors:
    BLUE = '\033[94m'
    CYAN = '\033[1;36m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    PURPLE = '\033[1;35m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD_GREEN = '\033[1;32m'

def print_text(text):
    print(text)

def print_yellow(text):
    print_text(bcolors.YELLOW + text + bcolors.ENDC)

def print_cyan(text):
    print_text(bcolors.CYAN + text + bcolors.ENDC)

def print_red(text):
    print_text(bcolors.RED + text + bcolors.ENDC)

def print_green(text):
    print_text(bcolors.GREEN + text + bcolors.ENDC)

# función para mostrar y ejecutar
def execute_cmd(cmd):
    print_yellow("\n\n[+] " + cmd)
    os.system(cmd)


# INTRO Y DATOS NECESARIOS
exec(open("config.py", encoding="utf-8").read())# cargar de archivo de configuración

os.system("dir hashes")# si no ejecuto algo no empiezan a salir los colores...
print_cyan(header)
print_cyan(description)

# pedir datos
print_cyan("\nPor defecto se utilizará el archivo de hashes = " + os.path.join(hashes_dir, hashes_file) + "\n")
hashes_file = input('Para elegir otro introdouce el nombre del archivo que se encuentre en el directorio ' + hashes_dir + ': ') or hashes_file
hashes_path = os.path.join(hashes_dir, hashes_file)

print_cyan(format_description)
hash_format = input('Introduce el nombre de la lista anterior o  el número correspondiente en hashcat al formato del hash: ') or hash_format
if hash_format in format_dictionary:
    hash_format = format_dictionary[hash_format]

print_cyan("\nPor defecto se utilizará el wordlist_custom =" + wordlist_custom)
wordlist_custom = input('\nSi quieres utilizar un minidiccionario específico para este proyecto introduce la ruta al archivo: ') or wordlist_custom

print_cyan("\nDATOS INTRODUCIDOS --> Archivo " + hashes_path + " con formato " + hash_format + " y diccionario personalizado " + wordlist_custom + " ...")

# mini manual de usuario
print_cyan(user_guide)
input('¿Empezamos? (dale al enter)')# para que dé tiempo a leer


# CRACKEO

print_cyan("\n\n1. PASAR WORDLISTS Y COMBINAR REGLAS: [-a 0 wordlist -r reglas -r reglas] (test, TEST, Test, .test, test2018, .test2018)\n")
execute_cmd(hashcat + "-m " + hash_format + " -a 0 " + hashes_path + wordlist_crackeados + wordlist_variado + wordlist_custom + " -r " + rules_super  + " -r " + rules_super + " --potfile-path " + potfile + options + debug)


print_cyan("\n\n2. PASAR WODRLISTS CON ATAQUE HIBRIDO POR LA DERECHA: [-a 6 wordlist ?d?l?u?s?a -i] (test9999, TEST9999, Test9999, test.., TEST.., Test..)\n")
execute_cmd(hashcat + "-m " + hash_format + " -a 6 " + hashes_path + wordlist_crackeados + wordlist_variado + wordlist_custom + "?d?d?d?d -j l -i --increment-min 1 --increment-max 4 --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 6 " + hashes_path + wordlist_crackeados + wordlist_variado + wordlist_custom + "?d?d?d?d -j u -i --increment-min 1 --increment-max 4 --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 6 " + hashes_path + wordlist_crackeados + wordlist_variado + wordlist_custom + "?d?d?d?d -j c -i --increment-min 1 --increment-max 4 --potfile-path " + potfile + options)

execute_cmd(hashcat + "-m " + hash_format + " -a 6 " + hashes_path + wordlist_crackeados + wordlist_variado + wordlist_custom + "?a?a? -j l -i --increment-min 1 --increment-max 2 --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 6 " + hashes_path + wordlist_crackeados + wordlist_variado + wordlist_custom + "?a?a? -j u -i --increment-min 1 --increment-max 2 --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 6 " + hashes_path + wordlist_crackeados + wordlist_variado + wordlist_custom + "?a?a? -j c -i --increment-min 1 --increment-max 2 --potfile-path " + potfile + options)


print_cyan("\n\n3. PASAR WODRLISTS CON ATAQUE HIBRIDO POR LA IZQUIERDA: [-a 7 ?d?l?u?s?a wordlist] (9999test, 9999TEST, 9999Test, ..test, ..TEST, ..Test)\n")
execute_cmd(hashcat + "-m " + hash_format + " -a 7 " + hashes_path + " ?d?d?d?d" + wordlist_crackeados + wordlist_variado + wordlist_custom + "-k l -i --increment-min 1 --increment-max 4 --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 7 " + hashes_path + " ?d?d?d?d" + wordlist_crackeados + wordlist_variado + wordlist_custom + "-k u -i --increment-min 1 --increment-max 4 --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 7 " + hashes_path + " ?d?d?d?d" + wordlist_crackeados + wordlist_variado + wordlist_custom + "-k c -i --increment-min 1 --increment-max 4 --potfile-path " + potfile + options)

execute_cmd(hashcat + "-m " + hash_format + " -a 7 " + hashes_path + " ?a?a" + wordlist_crackeados + wordlist_variado + wordlist_custom + "-k l -i --increment-min 1 --increment-max 2 --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 7 " + hashes_path + " ?a?a" + wordlist_crackeados + wordlist_variado + wordlist_custom + "-k u -i --increment-min 1 --increment-max 2 --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 7 " + hashes_path + " ?a?a" + wordlist_crackeados + wordlist_variado + wordlist_custom + "-k c -i --increment-min 1 --increment-max 2 --potfile-path " + potfile + options)


print_cyan("\n\n4. PASAR WORDLISTS COMBINADOS: [-a 1 wordlist wordlist] --> (testtest, testpassword, passwordtest, passwordpassword) VA A TARDAR y ni siquiera estoy utilizando reglas...\n")
execute_cmd(hashcat + "-m " + hash_format + " -a 1 " + hashes_path + wordlist_crackeados + wordlist_crackeados + " --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 1 " + hashes_path + wordlist_variado + wordlist_variado + " --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 1 " + hashes_path + wordlist_custom + wordlist_custom + " --potfile-path " + potfile + options)

execute_cmd(hashcat + "-m " + hash_format + " -a 1 " + hashes_path + wordlist_crackeados + wordlist_variado + " --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 1 " + hashes_path + wordlist_variado + wordlist_custom + " --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 1 " + hashes_path + wordlist_custom + wordlist_crackeados + " --potfile-path " + potfile + options)

execute_cmd(hashcat + "-m " + hash_format + " -a 1 " + hashes_path + wordlist_variado + wordlist_crackeados + " --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 1 " + hashes_path + wordlist_custom + wordlist_variado + " --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 1 " + hashes_path + wordlist_crackeados + wordlist_custom + " --potfile-path " + potfile + options)


print_cyan("\n\n5. PASAR WORDLISTS COMBINADOS CON REGLAS ESPECÍFICAS: [-a 1 wordlist wordlist] --> (SÓLO WORDLIST_VARIADO) Esto es mejor hacerlo a mano con lo que se te ocurra... (Testuser1, TestUser1, test.user, test_user)\n")
execute_cmd(hashcat + "-m " + hash_format + " -a 1 " + hashes_path + wordlist_variado + wordlist_variado + " -j c -k '$1' --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 1 " + hashes_path + wordlist_variado + wordlist_variado + " -j c -k 'c$1' --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 1 " + hashes_path + wordlist_variado + wordlist_variado + " -k \"^.\" -j \"^_$.\" --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 1 " + hashes_path + wordlist_variado + wordlist_variado + " -k \"^.\" --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 1 " + hashes_path + wordlist_variado + wordlist_variado + " -k \"^_\" --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 1 " + hashes_path + wordlist_variado + wordlist_variado + " -k \"^@\" --potfile-path " + potfile + options)


print_cyan("\n\n6. ATAQUE DE FUERZA BRUTA: [-a 3 ?1 -1?d?l?u?s?a] --> VA A TARDAR... (0aA, 0aA.) increment-min/increment-max: " + increment_min + "/" + increment_max)
execute_cmd(hashcat + "-m " + hash_format + " -a 3 " + hashes_path + " ?1?1?1?1?1?1?1?1?1?1 -1?d?l?u -i --increment-min " + increment_min + " --increment-max " + increment_max + " --potfile-path " + potfile + options)
execute_cmd(hashcat + "-m " + hash_format + " -a 3 " + hashes_path + " ?1?1?1?1?1?1?1?1?1?1 -1?a -i --increment-min " + increment_min + " --increment-max " + str(int(increment_max)-1) + " --potfile-path " + potfile + options)

# RESULTADOS
print_green("\n\nRESULTADO: hashes crackeados:")
cmd = hashcat + "-m " + hash_format + " -a 0 " + hashes_path + " --potfile-path" + potfile +  "--show" + options
print_yellow("\n\n[+] " + cmd)
print(bcolors.GREEN)
os.system(cmd)
print(bcolors.ENDC)