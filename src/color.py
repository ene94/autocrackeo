"""
 Print text and colors
"""

try:
	import sys
	from termcolor import colored
except Exception as e:
	sys.exit(" [X] " + str(e))

def showStarting(starting):
	print(colored("\n . . . " + starting + " . . . \n", 'cyan'))

def showEnding():
	print(colored("\n ¡ · · · Mischief managed · · ·  !\n", 'cyan'))

def showTitle(title):
	print(colored("\n-------- ~ ~ ~  " + title + "\n", 'cyan'))

def showException(exception, exit):
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	print(colored(" [X] " + filename + " in line: " + str(lineno) + " " + str(e), 'red'))
	if exit:
		sys.exit()

def showError(error, exit):
	print(colored(" [X] " + error, 'red'))
	if exit:
		sys.exit()

def showSuccess(success):
	print(colored(" [+] " + success, 'green'))

def showMessage(message):
	print(colored(" [*] " + message, 'yellow'))

def showVerbose(verbose):
	print("  · · · " + verbose)

def showCmd(verbose):
	print(colored("\n  · · · " + verbose, 'cyan'))