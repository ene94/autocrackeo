"""
 Print text and colors
"""

try:
	import sys
	import logging
	from termcolor import colored
except Exception as e:
	sys.exit(" [X] " + str(e))

class Color(object):

	def __init__(self):
		# set logger at start
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.INFO)
		self.fileHandler = None
		self.logFile = None
			
	# send logging to file
	
	def setFileHandler(self, logfile):
		self.logFile = logfile
		self.fileHandler = logging.FileHandler(logfile)
		self.fileHandler.setLevel(logging.INFO)
		self.logger.addHandler(self.fileHandler)

	# log text
	def logThis(self, text):
		self.logger.info(text)

	# -----------------------

	@staticmethod
	def showStarting(starting):
		print(colored("\n . . . " + starting + " . . . \n", 'cyan'))

	@staticmethod
	def showEnding():
		print(colored("\n ¡ · · · Mischief managed · · ·  !\n", 'cyan'))

	@staticmethod
	def showTitle(title):
		print(colored("\n-------- ~ ~ ~  " + title + "\n", 'cyan'))

	@staticmethod
	def showException(exception, exit=False):
		exc_type, exc_obj, tb = sys.exc_info()
		f = tb.tb_frame
		lineno = tb.tb_lineno
		filename = f.f_code.co_filename
		print(colored(" [X] " + filename + " in line: " + str(lineno) + " " + str(exception), 'red'))
		if exit:
			sys.exit()

	@staticmethod
	def showError(error, exit):
		print(colored(" [X] " + error, 'red'))
		if exit:
			sys.exit()

	@staticmethod
	def showSuccess(success):
		print(colored(" [+] " + success, 'green'))

	@staticmethod
	def showMessage(message):
		print(colored(" [*] " + message, 'yellow'))

	@staticmethod
	def showVerbose(verbose):
		#print("  · · · " + verbose)
		print("  . . . " + verbose)
		# specific for autocrackeo

	@staticmethod
	def showCmd(cmd):
		#print(colored("\n  · · · " + verbose, 'cyan'))
		print(colored("\n  . . . " + cmd, 'cyan'))

	@staticmethod
	def datetime_to_string(date_time):
		# ex. 20110104172008 -> Jan. 04, 2011 5:20:08pm 
		fmt = '%d/%m/%Y %H:%M:%S'
		date_time_string = date_time.strftime(fmt)
		return date_time_string

	@staticmethod
	def timedelta_to_string(time_delta):
		td = str(time_delta).split('.')[0]
		td = td.split(':')
		return "{0}h {1}m {2}s".format(td[0], td[1], td[2])