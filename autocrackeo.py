# -*- coding: utf-8 -*-
try:
	import os, sys, json, argparse, signal
	version = str(sys.version_info[0]) + "." + str(sys.version_info[1])
	if sys.version_info[0] < 3 or sys.version_info[1] < 6:
	    sys.exit("Python version must be at least 3.6, current is " + version)
	from datetime import datetime, timedelta
	from src.color import Color
	from src.configuration import Configuration
	from src.attacks import Attacks
	from src.hashcat import Hashcat
	from src.results import Results

except Exception as e:
	sys.exit(e)

def handler(signum, frame):
	"""
	 Handler for the SIGINT system's Ctrl+c signal
	 raise custom exception to skip all the attacks
	 and go straight to the results
	"""
	raise Exception("skip_attacks")# raise exception and throw in hashcat-->attacks-->autocrackeo --> catch there
	return

def get_arguments():
	"""
	 Manage input parameters
	"""
	parser = argparse.ArgumentParser(description="Automated Hashcat usage tool", epilog='Example: python3.6 autocrackeo.py -m 1000 hashes\\test.hash -c config\\quick_test.json -e="--username" -r')
	cmd = parser.add_argument("-m", type=str, dest="hash_type", help="hashcat's hash type number or its corresponding title, more info here: https://hashcat.net/wiki/doku.php?id=example_hashes", required=True)
	parser.add_argument("hash_file", type=str,  help="path to the file with hashes to crack")
	parser.add_argument("-e", "--extra-params", type=str, dest="extra_params", default="", help="extra params to add in the hashcat command", required=False)
	# or -c  execute attacks, or -r generate results, or both
	parser.add_argument("-c", "--config", type=str, dest="config_file", help="configuration (json) file to use with specific attacks")
	parser.add_argument("-r", "--results", action='store_true', help="shows a summary of the results and saves them to a file using the potfile")
	#parser.add_argument("-v", "--version", action='version', version='%(prog)s 1.1')
	return parser.parse_args()


if __name__ == "__main__":
	"""
	 configuration: all the config data
	 attacks: configure attacks from config data
	 hashcat: calls to hashcat individual attacks
	 results: generates a report with the results
	"""
	os.system("") # enable command colors
	print(Color.cyan("\n...AutoCrackeo..."))

	arguments = get_arguments()
	conf = Configuration(arguments.hash_file, arguments.hash_type, arguments.config_file, arguments.extra_params)
	results = Results(conf.static_values)
	hashcat = Hashcat(conf.static_values, results)
	attacks = Attacks(hashcat)

	if arguments.config_file: # if -c/--config
		"""
		 Execute a specific selection of hashcat attacks
		 previously defined on the configuration json file
		 This will be updated gradually as the efficiency of the attacks are measured
		"""
		# print start datetime
		start_date = datetime.now()
		print("\nStart date: " + Results.datetime_to_string(start_date) + "\n")

		"""
		 Set a SIGINT signal handler to securely skip all the attacks if the user wants to
		"""
		print(Color.cyan("Press Ctrl+c to skip attacks..."))
		signal.signal(signal.SIGINT, handler)

		try:
			print(Color.cyan("Press enter or 's' to see hashcat's status..."))
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
		except Exception as e:
			# if custom exception for exiting attacks --> continue from here
			if str(e) == "skip_attacks":
				print(Color.red(" --> Skipping attacks"))
			# else, show exception and exit
			else:
				Color.show_error(e)

		# print end datetime and duration
		end_date = datetime.now()
		print("\nEnd date: " + Results.datetime_to_string(end_date))
		duration = end_date - start_date
		print("Duration: " + Results.timedelta_to_string(duration))

	if arguments.results: # if -r/--results
		"""
		 Generate results files
		 Show results summary on screen
		"""
		hashcat.save_cracked()
		print(Color.yellow(results.get_summary()))

	if not arguments.config_file and not arguments.results:
		print(Color.red("\nNothing happening here... add [-c config_file] to execute attacks or [-r] to show results"))

	"""
	 Print end of execution
	"""	
	print(Color.yellow("\nMischief Managed!"))
