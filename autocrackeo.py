# -*- coding: utf-8 -*-
try:
	import os, sys, json, argparse
	version = str(sys.version_info[0]) + "." + str(sys.version_info[1])
	if sys.version_info[0] < 3 or sys.version_info[1] < 6:
	    sys.exit("Python version must be at least 3.6, current is " + version)
	from datetime import datetime, timedelta
	from src.color import Color
	from src.configuration import Configuration
	from src.attacks import Attacks
	from src.hashcat import Hashcat

	from pprint import pprint

except Exception as e:
	sys.exit(e)

def get_arguments():
	"""
	 Manage input parameters
	"""
	parser = argparse.ArgumentParser(description="Automated Hashcat usage tool", epilog='Examples:\npython3 autocrackeo.py -m 1000 -f hashes\\test.hash -c config\\quick_test.json -e="--username" -r -o .')
	
	# or hashfile + hashtype, or hash files list
	parser.add_argument("-m", type=str, dest="hash_type", help="hashcat's hash type number or its corresponding title, more info here: https://hashcat.net/wiki/doku.php?id=example_hashes")
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("-i", "--hash-file", type=str,  dest="hash_file", help="path to the file with hashes to crack")
	group.add_argument("-I", "--hash-files-list", type=str,  dest="hash_files", help="path to the json file with a list of hash files and types to crack")
	
	# -c  execute attacks
	parser.add_argument("-c", "--config", type=str, dest="config_file", help="configuration (json) filename to use with specific attacks (relative path from: /autocrackeo/config/, or absolute path")
	
	# -w use custom wordlist from custom path
	parser.add_argument("-w", "--wordlist-custom", type=str, dest="wordlist_custom_file", help="custom wordlist to use instead of default /autocrackeo/wordlists/custom.dic")

	# extra params to add at the end of the hashcat command
	parser.add_argument("-e", "--extra-params", type=str, dest="extra_params", default="", help="extra params to add in the hashcat command")
	parser.add_argument("-v", "--version", action='version', version='%(prog)s 1.4 (30/05/2019)')

	# output directory, default current dir
	parser.add_argument("-o", "--output-dir", type=str, dest="output_dir", default="", help="path to store the results (potfile.pot, cracked.txt, user_pwd.txt")
	return parser.parse_args()

def datetime_to_string(date_time):
	# ex. 20110104172008 -> Jan. 04, 2011 5:20:08pm 
	fmt = '%d/%m/%Y %H:%M:%S'
	date_time_string = date_time.strftime(fmt)
	return date_time_string

def timedelta_to_string(time_delta):
	td = str(time_delta).split('.')[0]
	td = td.split(':')
	return "{0}h {1}m {2}s".format(td[0], td[1], td[2])

if __name__ == "__main__":
	"""
	 configuration: all the config data
	 attacks: configure attacks from config data
	 hashcat: calls to hashcat individual attacks
	"""
	os.system("") # enable command colors
	print(Color.cyan("\n...AutoCrackeo..."))

	# print start datetime
	start_date = datetime.now()
	print(Color.yellow("\nStart date: " + datetime_to_string(start_date)))
	print("\nPress enter or 's' to see hashcat's status...")
	print("Press 'q' to skip one hashcat command...")
	print("Press Ctrl+c to skip all hashcat commands at once...")

	# get input arguments
	arguments = get_arguments()

	if not arguments.config_file:
		Color.show_error_text("\nNothing happening here... add [-c config_file] to execute attacks", True)


	"""
	 For every config_file in the list (all configs)
	"""
	config_files_list = Configuration.getConfigFilesArray(arguments.config_file)

	for config_file in config_files_list:

		"""
		 For every hash_file in the list, execute all the defined attacks in the config_file
		"""
		hash_files_list = Configuration.getHashFilesArray(arguments.hash_file, arguments.hash_type, arguments.extra_params, arguments.hash_files)

		for hash_file_item in hash_files_list:
			parsing_errors = False

			if hash_file_item:
				if hash_file_item["hash_file"]:
					hash_file = hash_file_item["hash_file"]
				else:
					parsing_errors = True
				if hash_file_item["hash_type"]:
					hash_type = hash_file_item["hash_type"]
				else:
					parsing_errors = True
				if len(hash_file_item) == 3 and hash_file_item["extra_params"]:
					extra_params = hash_file_item["extra_params"]
				else:
					extra_params = ""
			else:
				parsing_errors = True

			if parsing_errors:
				Color.show_error_text("Error in the files/types/extra_param parsing... skipping this file", False)
				break

			conf = Configuration(hash_file, hash_type, config_file, extra_params, arguments.output_dir, arguments.wordlist_custom_file)
			hashcat = Hashcat(conf.static_values)
			attacks = Attacks(hashcat)

			# print important info
			print(Color.yellow("\n-----------------------------------------------------------------------------------------------------------\n"))
			print(Color.yellow("config file: " + config_file))
			print(Color.yellow("hash file: " + hash_file))
			print(Color.yellow("hash type: " + hash_type))
			print(Color.yellow("extra params: " + extra_params))



			if config_file: # if -c/--config
				"""
				 Execute a specific selection of hashcat attacks
				 previously defined on the configuration json file
				 This will be updated gradually as the efficiency of the attacks are measured
				"""
				try:
					for attack_name in conf.attacks:
						print(Color.yellow("\n" + attack_name.replace("_"," ").title()))
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
				except KeyboardInterrupt:
					"""
					 Set a SIGINT signal handler 
					 to securely skip all the attacks for this hash_file and config_file
					 but it continues the loop
					"""
					print(Color.red(" --> Skipping attacks"))
				except Exception as e:
					Color.show_error(e)

				hashcat.save_cracked() # ALWAYS DUMP RESULTS: for every config file tried, and every hash file/type

	"""
	 Print end of execution
	"""	
	# print end datetime and duration
	end_date = datetime.now()
	print(Color.yellow("\nEnd date: " + datetime_to_string(end_date)))
	duration = end_date - start_date
	print(Color.yellow("Duration: " + timedelta_to_string(duration)))

	print(Color.yellow("\nMischief Managed!"))

def datetime_to_string(date_time):
	fmt = '%d/%m/%Y %H:%M:%S' # ex. 20110104172008 -> Jan. 04, 2011 5:20:08pm 
	date_time_string = date_time.strftime(fmt)
	return date_time_string