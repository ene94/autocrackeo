# -*- coding: utf-8 -*-
try:
	import os, sys, json, argparse
	from src.color import Color
	from src.configuration import Configuration
	from src.attacks import Attacks
	from src.hashcat import Hashcat
	from src.results import Results
except Exception as e:
	sys.exit(e)

def get_arguments():
	"""
	 Manage input parameters
	"""
	parser = argparse.ArgumentParser(description="Automated Hashcat usage tool", epilog='Example: python3.6 autocrackeo.py -m 1000 hashes\\test.hash --config config\\quick_test.json --extra-params="--username"')
	cmd = parser.add_argument("-m", type=str, dest="hash_type", help="hashcat's hash type number or its corresponding title, more info here: https://hashcat.net/wiki/doku.php?id=example_hashes", required=True)
	parser.add_argument("hash_file", type=str,  help="path to the file with hashes to crack")
	parser.add_argument("-c", "--config", type=str, dest="config_file", help="configuration json file to use with specific attacks", required=True)
	parser.add_argument("-e", "--extra-params", type=str, dest="extra_params", default="", help="extra params to add in the hashcat command", required=False)
	parser.add_argument("-r", "--just-results", action='store_true', help="skips the attacks and just shows the results using the potfile")
	parser.add_argument("-v", "--version", action='version', version='%(prog)s 1.0')
	return parser.parse_args()

if __name__ == "__main__":
	"""
	 configuration: all the config data
	 attacks: configure attacks from config data
	 hashcat: calls to hashcat individual attacks
	 results: generates a report with the results
	"""
	os.system("") # enable command colors
	arguments = get_arguments()
	conf = Configuration(arguments.hash_file, arguments.hash_type, arguments.config_file, arguments.extra_params)
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
	# SAVE --show and --left
	hashcat.save_cracked()
	hashcat.save_left()
	
	# PRINT SUMMARY
	print(Color.yellow(results.get_summary()))
	
	print(Color.yellow("\nMischief Managed!"))