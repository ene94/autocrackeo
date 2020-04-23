# -*- coding: utf-8 -*-
# Author: MaiShadow

"""
 Import modules
"""
try:
	import os, sys, json, argparse, logging
	version = str(sys.version_info[0]) + "." + str(sys.version_info[1])
	if sys.version_info[0] < 3 or sys.version_info[1] < 6:
	    sys.exit("[X] Python version must be at least 3.6, current is " + version)

	from datetime import datetime, timedelta
	from src.color import Color
	from src.configuration import Configuration
	from src.attacks import Attacks
	from src.hashcat import Hashcat

except Exception as e:
	sys.exit(" [X] " + str(e))

"""
 Manage input parameters
"""
def getArguments():
	parser = argparse.ArgumentParser(description="Automated Hashcat usage tool", epilog='Usage: python3 autocrackeo.py -m 1000 -i docs\\test_files\\ntlm.hash -w docs\\test_files\\custom.dic -o docs\\test_files\\results -c all -e="--username" --feedback --verbose')
	
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
	
	# other functionalities
	parser.add_argument("--feedback", action="store_true", dest="feedback", help="dump plaintext passwords from potfile (-o) to custom wordlist (-w)")
	parser.add_argument("-v", "--verbose", action='store_true', dest="verbose", help="show more messages")
	parser.add_argument("--version", action='version', version='%(prog)s 1.6 (07/03/2020)')

	# output directory, default current dir
	parser.add_argument("-o", "--output-dir", type=str, dest="output_dir", default="", help="path to store the results (potfile.pot, cracked.txt, user_pwd.txt")
	return parser.parse_args()

def main(color):
	"""
	 configuration: all the config data
	 attacks: configure attacks from config data
	 hashcat: calls to hashcat individual attacks
	"""

	# print start datetime
	start_date = datetime.now()
	Color.showVerbose("Start date: " + Color.datetime_to_string(start_date))
	Color.showVerbose("Press enter or [s] to see hashcat's status...")
	Color.showVerbose("Press [q]' to skip one hashcat command...")
	Color.showVerbose("Press [Ctrl+c] to skip all hashcat commands at once...")

	# get input arguments
	arguments = getArguments()

	if not arguments.config_file:
		Color.showError("Nothing happening here... add [-c config_file] to execute attacks", True)


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
				Color.showError("Error in the files/types/extra_param parsing... skipping this file", False)
				break

			# load other scripts
			conf = Configuration(hash_file, hash_type, config_file, extra_params, arguments.output_dir, arguments.wordlist_custom_file)
			hashcat = Hashcat(conf.static_values, arguments.verbose, color)
			attacks = Attacks(hashcat)

			# print important info
			Color.showTitle("")
			msg = "Attacks config file:" + config_file + ", hash file:" + hash_file + ", hash type:" + hash_type + ", extra params:" + extra_params
			Color.showMessage(msg  + "\n")

			# set logging config
			color.setFileHandler(os.path.join(conf.results_dir, "autocrackeo.log")) # set log file for every hash file
			color.logThis("[i] " + Color.datetime_to_string(datetime.now()) + ", " + msg)

			if config_file: # if -c/--config
				"""
				 Execute a specific selection of hashcat attacks
				 previously defined on the configuration json file
				 This will be updated gradually as the efficiency of the attacks are measured
				"""
				try:
					for attack_name in conf.attacks:
						if arguments.verbose: Color.showVerbose("Attack type: " + attack_name.replace("_"," ").title())
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
							Color.showError("This attack name is not recognized!", False)

						# dump plaintext passwords from potfile to custom wordlist
						if arguments.feedback: hashcat.feedback(arguments.wordlist_custom_file)

				except KeyboardInterrupt:
					"""
					 Set a SIGINT signal handler 
					 to securely skip all the attacks for this hash_file and config_file
					 but it continues the loop
					"""
					Color.showError("Skipping attacks", False)
					color.logThis("[X] Ctrl+C: Skipping attacks...")
				except Exception as e:
					Color.showException(e, True)

				hashcat.save_cracked() # ALWAYS DUMP RESULTS: for every config file tried, and every hash file/type

	"""
	 Print end of execution
	"""	
	# print end datetime and duration
	Color.showTitle("")
	end_date = datetime.now()
	Color.showVerbose("End date: " + Color.datetime_to_string(end_date))
	duration = end_date - start_date
	Color.showVerbose("Duration: " + Color.timedelta_to_string(duration))

"""
 Call main method
"""
if __name__ == '__main__':
	os.system("") # do nothing but enable command colors on windows cmd
	color = Color()
	Color.showTitle("Autocrackeo")
	try:
		main(color)
	except Exception as e:
		Color.showException(e, True)
	Color.showEnding()