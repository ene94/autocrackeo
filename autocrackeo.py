# -*- coding: utf-8 -*-
try:
	import os, sys, json, argparse
	from src.color import Color
	from src.attacks import Attacks
	from src.hashcat import Hashcat
	from src.results import Results
except Exception as e:
	sys.exit(e)

def get_arguments():
	"""
	 Manage input parameters
	"""
	parser = argparse.ArgumentParser(description="Automated Hashcat usage tool", epilog="Example: python3 autocrackeo.py -m 1000 hashes\\test.hash --config src\config.json")
	cmd = parser.add_argument("-m", type=str, dest="hash_type", help="hashcat's hash type number, more info here: https://hashcat.net/wiki/doku.php?id=example_hashes", required=True)
	parser.add_argument("hash_file", type=str,  help="path to the file with hashes to crack")
	parser.add_argument("--config", type=str, dest="config_file", help="configuration json file to use with specific attacks", required=True)
	parser.add_argument("--just-results", action='store_true', help="skips the attacks and just shows the results using the potfile")
	parser.add_argument('--version', action='version', version='%(prog)s 1.0')
	return parser.parse_args()

class Configuration(object):
	"""
	 Gather all the information and configuration the program is going to use
	"""
	def __init__(self, hash_file, hash_type, config_file):
		conf = None
		try:
			with open(os.path.join(config_file), "r") as f:
				conf = json.load(f)

			"""
			 Load paths and parameters from config file
			 And add the relative paths to the files to use
			"""			
			#static parameters
			self.attacks = conf["attacks"]
			self.paths = conf["paths"]
			self.static_values = conf["parameters"]
			self.wordlists, self.rules,self.masks = [], [], []

			if self.static_values["resources"]["resource_level"] == "low":
				self.static_values["resource_options"] = self.static_values["resources"]["resource_low"]
			else:
				self.static_values["resource_options"] = self.static_values["resources"]["resource_high"]
			self.static_values["pot_file"] = os.path.join(self.paths["results_dir"], "potfile.pot")
			self.static_values["out_file"] = os.path.join(self.paths["results_dir"], "plaintext_passwords.txt")
			self.static_values["out_file_cracked"] = os.path.join(self.paths["results_dir"], "hashes_cracked.txt")
			self.static_values["out_file_left"] = os.path.join(self.paths["results_dir"], "hashes_left.txt")
			#self.static_values["report_file"] = os.path.join(self.paths["results_dir"], self.static_values["results_files"]["report_file"])

			#path to the files
			for wordlist in self.static_values["wordlists_files"]:
				self.wordlists.append(os.path.join(self.paths["wordlists_dir"], wordlist))

			for rules_file in self.static_values["rules_files"]:
				self.rules.append(os.path.join(self.paths["rules_dir"], rules_file))

			for masks_file in self.static_values["masks_files"]:
				self.masks.append(os.path.join(self.paths["masks_dir"], masks_file))

			# check that files exist
			file_paths = self.wordlists + self.rules + self.masks
			for file_path in file_paths:
				f = os.path.isfile(file_path)

			"""
			 Load parameters from input arguments
			"""
			self.static_values["hash_type"] = hash_type
			self.static_values["hash_file"] = hash_file
			self.static_values["config_file"] = config_file

		except Exception as e:
			Color.show_error(e)

if __name__ == "__main__":
	"""
	 configuration: all the config data
	 attacks: configure attacks from config data
	 hashcat: calls to hashcat individual attacks
	 results: generates a report with the results
	"""
	os.system("") # enable command colors
	arguments = get_arguments()
	conf = Configuration(arguments.hash_file, arguments.hash_type, arguments.config_file)
	results = Results(conf.static_values)
	hashcat = Hashcat(conf.static_values, results)
	attacks = Attacks(hashcat)

	if arguments.just_results == False:

		"""
		 Execute a specific selection of hashcat attacks
		 previously defined on the configuration json file
		 This will be updated gradually as the efficiency of the attacks are measured
		"""
		print(Color.cyan("Press enter or 's' to see hashcat's status..."))
		for attack_name in conf.attacks:
			print(Color.yellow("\n" + attack_name))
			if "straight" in attack_name:
				attacks.straight_attacks(attack_name, conf.attacks[attack_name], conf.wordlists, conf.rules)
			elif "combinator" in attack_name:
				attacks.combinator_attacks(attack_name, conf.attacks[attack_name], conf.wordlists)
			elif "brute_force" in attack_name:
				attacks.brute_force_attacks(attack_name, conf.attacks[attack_name], conf.masks)
			elif "hybrid" in attack_name:
				attacks.hybrid_attacks(attack_name, conf.attacks[attack_name], conf.wordlists, conf.masks)
			elif "one_word_per_hash" in attack_name:
				attacks.OneWordPerHashAttacks(attack_name, conf.attacks[attack_name], conf.wordlists)
			else:
				print(Color.red("This attack name is not recognized!"))

	"""
	 Generate results files
	 Show results on screen
	"""
	# SAVE
	hashcat.save_cracked()
	hashcat.save_left()
	
	# PRINT SUMMARY
	print(Color.yellow(results.get_summary()))
	
	print(Color.yellow("\nMischief Managed!"))