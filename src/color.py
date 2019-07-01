import sys

class Color:
	"""
	Print text with colors
	"""

	CYAN = '\033[1;36m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	END = '\033[0m'

	@staticmethod
	def yellow(text):
		return Color.YELLOW + text + Color.END

	@staticmethod
	def cyan(text):
		return Color.CYAN + text + Color.END

	@staticmethod
	def red(text):
		return Color.RED + text + Color.END

	@staticmethod
	def green(text):
		return Color.GREEN + text + Color.END
	
	@staticmethod
	def show_error(e):
		"""
		Show exceptions
		"""
		exc_type, exc_obj, tb = sys.exc_info()
		f = tb.tb_frame
		lineno = tb.tb_lineno
		filename = f.f_code.co_filename
		print(Color.red("ERROR: " + filename + " in line: " + str(lineno) + " " + str(e)))
		sys.exit()

	@staticmethod
	def show_error_text(text, exit):
		"""
		Show custom error message
		"""
		print(Color.red("ERROR: " + text))
		if exit:
			sys.exit()

