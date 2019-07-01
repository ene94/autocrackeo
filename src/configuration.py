# -*- coding: utf-8 -*-
try:
	import os, sys, json
	from src.color import Color
	from pprint import pprint
except Exception as e:
	sys.exit(e)

class Configuration(object):
	"""
	 Gather all the information and configuration the program is going to use
	"""
	def __init__(self, hash_file, hash_type, config_file, extra_params, output_dir, wordlist_custom_dir):
		conf = None
		hostconf = None
		self.attacks = {}
		self.static_values = {}

		"""
		 Configure working paths
		"""
		# ....../autocrackeo/src/configuration.py --> ......./autocrackeo/
		base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))	# print("base_dir: " + base_dir)
		self.config_dir = os.path.join(base_dir, "config")
		self.wordlists_dir = os.path.join(base_dir, "wordlists") 	# base_dir = D:\NEVADA\
		self.rules_dir = os.path.join(base_dir, "rules")			# base_dir = D:\NEVADA\
		self.masks_dir = os.path.join(base_dir, "masks")			# base_dir = D:\NEVADA\
		self.source_dir = os.path.join(base_dir, "src")

		# configure results dir and create folder if not exists
		if output_dir:
			self.results_dir = os.path.join(output_dir)				# base_dir = D:\NEVADA\proyectos\{nombre_proyecto}\
		else:
			self.results_dir = os.path.join(".")  					# if not selected, make current dir .
		try:
			if not os.path.exists(self.results_dir):
				os.makedirs(self.results_dir)
		except OSError as e:
			Color.show_error(e)

		try:
			"""
			 Load hashcat execution parameters from host-config file
			"""
			#read and extract json data
			with open(os.path.join(self.config_dir, "HOST_CONFIG.json"), "r", encoding="utf-8") as f:
				hostconf = json.load(f)

			# host config: executable, resources
			self.static_values["executable"] = hostconf["executable"]
			if hostconf["resources"]["resource_level"] == "low_windows":
				self.static_values["resource_options"] = hostconf["resources"]["resource_low_windows"]
			elif hostconf["resources"]["resource_level"] == "low_kali":
				self.static_values["resource_options"] = hostconf["resources"]["resource_low_kali"]
			else:
				self.static_values["resource_options"] = hostconf["resources"]["resource_high"]

			"""
			 Load parameters from input arguments
			"""
			# generate filename for cracked results
			self.static_values["hash_file"] = hash_file
			hash_file_name = hash_file.split(os.path.sep)[-1] # last part of the hash list path: hashfile name
			cracked_file_name = "cracked-" + hash_type + "-" + hash_file_name.replace(".", "_") + ".txt"
			cracked_file_name = cracked_file_name.lower()
			self.static_values["out_file_cracked"] = os.path.join(self.results_dir, cracked_file_name)
			hash_type = self.checkHashType(hash_type)
			self.static_values["hash_type"] = hash_type
			self.static_values["config_file"] = config_file
			self.static_values["extra_params"] = extra_params

			# Define potfile
			pot_file = os.path.join(self.results_dir, "potfile.pot")
			self.static_values["pot_file"] = pot_file

			# Check needed file existence
			file_paths = [hash_file]
			for file_path in file_paths:
				exists = os.path.isfile(file_path)
				if not exists:
					Color.show_error_text("File {file_path} does not exist...".format(file_path=file_path), True)

			"""
			 Load attacks and useful files from config file
			 And add the relative paths to the files to use
			"""

			if config_file:
				# load /autocrackeo/config/ + {config_file}
				config_path = os.path.join(self.config_dir, config_file) # print(config_path)
				with open(config_path, "r", encoding="utf-8") as f:
					conf = json.load(f)

					self.wordlists, self.rules,self.masks = [], [], []
					self.attacks = conf["attacks"]
					self.static_values.update(conf["files"])

					# path to the files:
					## wordlists
					for wordlist in self.static_values["wordlists_files"]:
						if wordlist_custom_dir and wordlist and wordlist == "custom.dic":
							self.wordlists.append(os.path.join(wordlist_custom_dir)) # if input argument -w custom_wordlist.txt replace default custom.dic
						else:
							self.wordlists.append(os.path.join(self.wordlists_dir, wordlist))
					
					## rules
					for rules_file in self.static_values["rules_files"]:
						self.rules.append(os.path.join(self.rules_dir, rules_file))

					## masks
					for masks_file in self.static_values["masks_files"]:
						self.masks.append(os.path.join(self.masks_dir, masks_file))

			#pprint(self.static_values)# mostrar contenido del objeto

		except Exception as e:
			Color.show_error(e)

	def checkHashType(self, hash_type):
		"""
		Check if input hash type is a...
			correct number
			valid string corresponding a hash type number in the hash_types.json file

		"""
		try:
			# if it is already a valid number
			if hash_type.isdigit() and int(hash_type) in range(0,99999):
				return hash_type
			# if it is a string with the title of the format
			else:
				with open(os.path.join(self.source_dir, "hash_types.json"), "r", encoding="utf-8") as f:
					types = json.load(f)
				lower_keys =  {k.lower(): v for k,v in types.items()} #r take ['MD5': '0'...] and return ['md5': '0']
				hash_type = hash_type.lower() # lower input type MD5 to md5
				if hash_type in lower_keys.keys():
					return lower_keys[hash_type]
				else:
					Color.show_error_text("Invalid hash type number or title. Check valid list here: https://hashcat.net/wiki/doku.php?id=example_hashes", True)

		except Exception as e:
			Color.show_error(e)

	@staticmethod
	def getHashFilesArray(hash_file, hash_type, extra_params, hash_files):
		# get hash_files, hash_types, and extra_params from input params
		if hash_file:
			if hash_type:
				if extra_params == None:
					extra_params = ""
				hash_files_list = [{"hash_file": hash_file, "hash_type": hash_type, "extra_params": extra_params}]
			else:
				Color.show_error_text("Error: the argument -m [HASH_TYPE] is required", True)
		# or get hash_files, hash_types, and extra_params from json file
		elif hash_files:
			hash_files_list = Configuration.parseHashFilesList(hash_files)
		return hash_files_list


	@staticmethod
	def parseHashFilesList(hash_files_list_path):
		"""
		 Parse hash files list with the hash_file, hash_type, extra_params in json format
		"""
		try:

			with open(hash_files_list_path, "r", encoding="utf-8") as f:
				json_file = json.load(f)
				files_list = json_file["list"]
				return files_list

		except Exception as e:
			Color.show_error(e)

	@staticmethod
	def getConfigFilesArray(config_file):
		if config_file:
			if config_file == "all":
				config_files_list = Configuration.parseConfigFilesList(config_file + ".json")			
			else:
				config_files_list = [config_file]

			return config_files_list
		else:
			Color.show_error_text("Invalid ConfigFile", True)

	@staticmethod
	def parseConfigFilesList(all_configs_file):
		"""
		 Parse config_files list from json file
		"""
		try:
			path = os.path.join(Configuration.getBaseDir(), "config", all_configs_file)
			with open(path, "r", encoding="utf-8") as f:
				json_file = json.load(f)
				files_list = json_file["config_files"]
				return files_list

		except Exception as e:
			Color.show_error(e)

	@staticmethod
	def getBaseDir():
		base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))	# print("base_dir: " + base_dir)
		return base_dir