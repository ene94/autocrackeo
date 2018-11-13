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
	def __init__(self, hash_file, hash_type, config_file, extra_params):
		conf = None
		hostconf = None
		self.attacks = {}
		self.static_values = {}

		try:
			"""
			 Load paths and hashcat execution parameters from host-config file
			"""
			with open(os.path.join("config", "host-config.json"), "r") as f:
				hostconf = json.load(f)

			# host config: folders paths, executable, resources, potfile
			self.paths = hostconf["paths"]
			self.static_values["executable"] = hostconf["executable"]
			if hostconf["resources"]["resource_level"] == "low":
				self.static_values["resource_options"] = hostconf["resources"]["resource_low"]
			else:
				self.static_values["resource_options"] = hostconf["resources"]["resource_high"]

			"""
			 Load parameters from input arguments
			"""
			self.static_values["hash_file"] = hash_file
			hash_file_name = hash_file.split(os.path.sep)[-1] # last part of the hash list path: hashfile name
			self.static_values["out_file_cracked"] = os.path.join(self.paths["results_dir"], hash_file_name + "." + hash_type + ".res")
			hash_type = self.checkHashType(hash_type)
			self.static_values["hash_type"] = hash_type
			self.static_values["config_file"] = config_file
			self.static_values["extra_params"] = extra_params

			# Define potfile
			pot_file = os.path.join(self.paths["results_dir"], "potfile.pot")
			self.static_values["pot_file"] = pot_file

			# Check needed file existence
			file_paths = [hash_file, pot_file]
			for file_path in file_paths:
				exists = os.path.isfile(file_path)
				if not exists:
					Color.show_error_text("File {file_path} does not exist...".format(file_path=file_path))

			"""
			 Load attacks and useful files from config file
			 And add the relative paths to the files to use
			"""

			if config_file:
				with open(os.path.join(config_file), "r") as f:
					conf = json.load(f)

					self.wordlists, self.rules,self.masks = [], [], []
					self.attacks = conf["attacks"]
					self.static_values.update(conf["files"])

					# path to the files
					for wordlist in self.static_values["wordlists_files"]:
						self.wordlists.append(os.path.join(self.paths["wordlists_dir"], wordlist))

					for rules_file in self.static_values["rules_files"]:
						self.rules.append(os.path.join(self.paths["rules_dir"], rules_file))

					for masks_file in self.static_values["masks_files"]:
						self.masks.append(os.path.join(self.paths["masks_dir"], masks_file))

					# check if files exist --> less important
					file_paths = self.wordlists + self.rules + self.masks
					for file_path in file_paths:
						exists = os.path.isfile(file_path)
						if not exists:
							Color.show_error_text("File {file_path} does not exist...".format(file_path=file_path))

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
				with open(os.path.join("src", "hash_types.json"), "r") as f:
					types = json.load(f)
				if hash_type in types.keys():
					return types[hash_type]
				else:
					Color.show_error_text("Invalid hash type number or title. Check valid list here: https://hashcat.net/wiki/doku.php?id=example_hashes")

		except Exception as e:
			Color.show_error(e)