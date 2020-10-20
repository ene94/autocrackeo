# -*- coding: utf-8 -*-
try:
	import os, sys, json
	from src.color import Color
except Exception as e:
	sys.exit(e)

class Configuration(object):
	"""
	 Gather all the information and configuration the program is going to use
	"""
	def __init__(self, hash_file, hash_type, attacks_file, extra_params, output_dir, wordlist_custom_dir):
		self.color = Color()
		conf = None
		hostconf = None
		self.attacks = {}
		self.static_values = {}

		"""
		 Configure working paths
		"""
		# ....../autocrackeo/src/configuration.py --> ......./autocrackeo/
		base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))	# print("base_dir: " + base_dir)
		self.attacks_dir = os.path.join(base_dir, "attacks")
		self.wordlists_dir = os.path.join(base_dir, "wordlists")
		self.rules_dir = os.path.join(base_dir, "rules")
		self.masks_dir = os.path.join(base_dir, "masks")
		self.source_dir = os.path.join(base_dir, "src")

		# configure results dir and create folder if not exists
		if output_dir:
			self.results_dir = os.path.join(output_dir)
		else:
			self.results_dir = os.path.join(".")# if not selected, make current dir .
		try:
			if not os.path.exists(self.results_dir):
				os.makedirs(self.results_dir)
		except OSError as e:
			Color.showException(e)

		try:
			"""
			 Load hashcat execution parameters from host-config file
			"""
			#read and extract json data
			with open(os.path.join(self.source_dir, "HOST_CONFIG.json"), "r", encoding="utf-8") as f:
				hostconf = json.load(f)

			# host config: executable, resources
			self.static_values["executable"] = hostconf["executable"]
			self.static_values["resource_options"] = hostconf["resources"]

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
			self.static_values["attacks_file"] = attacks_file
			self.static_values["extra_params"] = extra_params

			# Define potfile
			pot_file = os.path.join(self.results_dir, "potfile.pot")
			self.static_values["pot_file"] = pot_file

			# Check needed file existence
			file_paths = [hash_file]
			for file_path in file_paths:
				exists = os.path.isfile(file_path)
				if not exists:
					Color.showError("File {file_path} does not exist...".format(file_path=file_path), True)

			"""
			 Load attacks and useful files from attacks json file
			 And add the relative paths to the files to use
			"""

			if attacks_file:
				# load /autocrackeo/attacks/ + {attacks_file}
				attacks_path = os.path.join(self.attacks_dir, attacks_file)
				with open(attacks_path, "r", encoding="utf-8") as f:
					conf = json.load(f)

					self.wordlists, self.rules,self.masks = [], [], []
					self.attacks = conf["attacks"]
					self.static_values.update(conf["files"])

					# path to the files:
					## wordlists
					for wordlist in self.static_values["wordlists_files"]:
						if wordlist:
							if wordlist != "custom.txt":
								self.wordlists.append(os.path.join(self.wordlists_dir, wordlist))
							else:
								if wordlist_custom_dir:
									self.wordlists.append(os.path.join(wordlist_custom_dir)) # if input argument -w custom_wordlist.txt replace default custom.txt
								else:
									self.wordlists.append(os.path.join(self.wordlists_dir,"super.txt")) # else take super.txt by default instead of custom.txt wordlist
									
							
					
					## rules
					for rules_file in self.static_values["rules_files"]:
						self.rules.append(os.path.join(self.rules_dir, rules_file))

					## masks
					for masks_file in self.static_values["masks_files"]:
						self.masks.append(os.path.join(self.masks_dir, masks_file))

			#pprint(self.static_values)# mostrar contenido del objeto

		except Exception as e:
			Color.showException(e)

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
					Color.showError("Invalid hash type number or title. Check valid list here: https://hashcat.net/wiki/doku.php?id=example_hashes", True)

		except Exception as e:
			Color.showException(e)

	@staticmethod
	def getHashFilesArray(hash_file, hash_type, extra_params, hash_files):
		# get hash_files, hash_types, and extra_params from input params
		if hash_file:
			if hash_type:
				if extra_params == None:
					extra_params = ""
				hash_files_list = [{"hash_file": hash_file, "hash_type": hash_type, "extra_params": extra_params}]
			else:
				Color.showError("Error: the argument -m [HASH_TYPE] is required", True)
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
			Color.showException(e)

	@staticmethod
	def getConfigFilesArray(attack_file):
		if attack_file:
			if attack_file == "all":
				attack_file_list = Configuration.parseConfigFilesList(attack_file + ".json")			
			else:
				attack_file_list = [attack_file + ".json"]

			return attack_file_list
		else:
			Color.showError("Invalid attacks config file", True)

	@staticmethod
	def parseConfigFilesList(all_attacks_file):
		"""
		 Parse attacks_files list from json file
		"""
		try:
			path = os.path.join(Configuration.getBaseDir(), "attacks", all_attacks_file)
			with open(path, "r", encoding="utf-8") as f:
				json_file = json.load(f)
				files_list = json_file["attacks_files"]
				return files_list

		except Exception as e:
			Color.showException(e)

	@staticmethod
	def getBaseDir():
		base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))	# print("base_dir: " + base_dir)
		return base_dir