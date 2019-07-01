# -*- coding: utf-8 -*-
try:
	import subprocess
	from src.color import Color
except Exception as e:
	sys.exit(e)

class Hashcat(object):
	"""
	Communicate with hashcat to execute commands
	Usage: hashcat [options]... hash|hashfile|hccapxfile [dictionary|mask|directory]...
	"""
	def __init__(self, conf):
		"""
		Storage for all posible parameters used by hashcat commands
		"""

		# static params
		self.executable = conf["executable"]
		self.hash_type = "-m " + conf["hash_type"]
		self.hash_file = conf["hash_file"]
		self.pot_file = "--potfile-path \"" + conf["pot_file"] + "\""
		#self.out_file = "-o " + conf["out_file"]
		self.out_file_format_pwd = "--outfile-format 2"# 2 pwd o 3 hash:pwd # si se añade --username será user:hash:pwd
		self.out_file_format_hash = "--outfile-format 1"# only hash
		self.resource_options = conf["resource_options"]
		self.extra_params = conf["extra_params"] or ""
		self.quiet = "--quiet"

		# dynamic params
		self.attack_mode = "-a {mode}"
		self.rules_file = "-r {rules_file}"
		self.rules_left = "-j \"{rules_left}\""
		self.rules_right = "-k \"{rules_right}\""
		self.increment = "-i"
		self.increment_min = "--increment-min {min}"
		self.increment_max = "--increment-max {max}"
		self.show = "--show"
		self.left = "--left"
		self.username = "--username"

		"""
		To save results when hashcat is called
		"""
		self.out_file_cracked_path = conf["out_file_cracked"]

	def getStaticPart(self):
		"""
		Return a string containing hashcat commands' static parameters
		"""
		return f"{self.executable} {self.hash_type} \"{self.hash_file}\" {self.pot_file} {self.out_file_format_pwd} {self.resource_options} {self.extra_params} {self.quiet} "

	def execute(self, cmd):
		"""
		Execute a os command with given string
		"""
		print(Color.cyan("\n" + cmd))
		p = subprocess.call(cmd, shell=True)

		'''
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
		(output, err) = p.communicate()
		p_status = p.wait()
		#print("Command output: ", output)
		#print("Command exit status/return code: ", p_status)
		'''
		return

	def straight(self, wordlist):
		"""
		Call hashcat's straight attack: -a 0
		"""
		attack_mode = f"{self.attack_mode}".format(mode=0)
		attack = "{attack_mode} \"{wordlist}\"".format(attack_mode=attack_mode, wordlist=wordlist)
		cmd = self.getStaticPart() + attack
		self.execute(cmd)
		return
	
	def straight_with_rules_manual(self, wordlist, rules_manual=":"):
		"""
		Call hashcat's straight attack with manual rules: -a 0 -j rules
		"""
		attack_mode = self.attack_mode.format(mode=0)
		rules_left = self.rules_left.format(rules_left=rules_manual)
		attack = "{attack_mode} \"{wordlist}\" {rules_left}".format(attack_mode=attack_mode, wordlist=wordlist, rules_left=rules_left)
		cmd = self.getStaticPart() + attack
		self.execute(cmd)
		return

	def straight_with_rules_file(self, wordlist, rules_file):
		"""
		Call hashcat's straight attack with rules file: -a 0 -r rules
		"""
		attack_mode = self.attack_mode.format(mode=0)
		rules_file = self.rules_file.format(rules_file=rules_file)
		attack = "{attack_mode} \"{wordlist}\" {rules_file}".format(attack_mode=attack_mode, wordlist=wordlist, rules_file=rules_file)
		cmd = self.getStaticPart() + attack
		self.execute(cmd)
		return

	def straight_with_combined_rules_files(self, wordlist, rules_file1, rules_file2):
		"""
		Call hashcat's straight attack with two rule files combined: -a 0 -r rules -r rules
		"""
		attack_mode = self.attack_mode.format(mode=0)
		rules_file1 = self.rules_file.format(rules_file=rules_file1)
		rules_file2 = self.rules_file.format(rules_file=rules_file2)
		attack = "{attack_mode} \"{wordlist}\" {rules_file1} {rules_file2}".format(attack_mode=attack_mode, wordlist=wordlist, rules_file1=rules_file1, rules_file2=rules_file2)
		cmd = self.getStaticPart() + attack
		self.execute(cmd)
		return

	def combinator(self, wordlist1, wordlist2, rules_left=":", rules_right=":"):
		"""
		Call hashcat's combinator attack: -a 1 wordlist wordlist -j rules_left -k rules_right
		"""
		attack_mode = self.attack_mode.format(mode=1)
		rules_left = self.rules_left.format(rules_left=rules_left)
		rules_right = self.rules_right.format(rules_right=rules_right)
		attack = "{attack_mode} \"{wordlist1}\" \"{wordlist2}\" {rules_left} {rules_right}".format(attack_mode=attack_mode, wordlist1=wordlist1, wordlist2=wordlist2, rules_left=rules_left, rules_right=rules_right)
		cmd = self.getStaticPart() + attack
		self.execute(cmd)
		return

	def brute_force_automatic(self, increment_min=False, increment_max=False):
		"""
		Call hashcat's brute force automatic attack: -a 3 [-i --increment-min num --increment-max num]
		"""
		attack_mode = self.attack_mode.format(mode=3)
		if increment_min==False and increment_max==False:
			attack = "{attack_mode}".format(attack_mode=attack_mode)
		else:
			increment = self.increment
			increment_min = self.increment_min.format(min=increment_min)
			increment_max = self.increment_max.format(max=increment_max)
			attack = "{attack_mode} {increment} {increment_min} {increment_max}".format(attack_mode=attack_mode, increment=increment, increment_min=increment_min, increment_max=increment_max)
		cmd = self.getStaticPart() + attack
		self.execute(cmd)
		return

	def brute_force(self, masks, increment_min=False, increment_max=False):
		"""
		Call hashcat's brute force automatic attack: -a 3 masks [-i --increment-min num --increment-max num]
		"""
		attack_mode = self.attack_mode.format(mode=3)
		if increment_min==False and increment_max==False:
			attack = "{attack_mode} {masks}".format(attack_mode=attack_mode, masks=masks)
		else:
			increment = self.increment
			increment_min = self.increment_min.format(min=increment_min)
			increment_max = self.increment_max.format(max=increment_max)
			attack = "{attack_mode} {masks} {increment} {increment_min} {increment_max}".format(attack_mode=attack_mode, masks=masks, increment=increment, increment_min=increment_min, increment_max=increment_max)
		cmd = self.getStaticPart() + attack
		self.execute(cmd)
		return

	def hybrid_right(self, wordlist, masks, rules_left=":", increment_min=False, increment_max=False):
		"""
		Call hashcat's hybrid attack (wordlist + right mask): -a 3 wordlist masks -j rules [-i --increment-min num --increment-max num]
		"""
		attack_mode = self.attack_mode.format(mode=6)
		rules_left = self.rules_left.format(rules_left=rules_left)
		if increment_min==False and increment_max==False:
			attack = "{attack_mode} \"{wordlist}\" {masks} {rules_left}".format(attack_mode=attack_mode, wordlist=wordlist, masks=masks, rules_left=rules_left)
		else:
			increment = self.increment
			increment_min = self.increment_min.format(min=increment_min)
			increment_max = self.increment_max.format(max=increment_max)
			attack = "{attack_mode} \"{wordlist}\" {masks} {rules_left} {increment} {increment_min} {increment_max}".format(attack_mode=attack_mode, wordlist=wordlist, rules_left=rules_left, masks=masks, increment=increment, increment_min=increment_min, increment_max=increment_max)
		cmd = self.getStaticPart() + attack
		self.execute(cmd)
		return

	def hybrid_left(self, wordlist, masks, rules_right=":", increment_min=False, increment_max=False):
		"""
		Call hashcat's hybrid attack (left mask + wordlis): -a 3 masks wordlist -k rules [-i --increment-min num --increment-max num]
		"""
		attack_mode = self.attack_mode.format(mode=7)
		rules_right = self.rules_right.format(rules_right=rules_right)
		if increment_min==False and increment_max==False:
			attack = "{attack_mode} {masks} \"{wordlist}\" {rules_right}".format(attack_mode=attack_mode, wordlist=wordlist, masks=masks, rules_right=rules_right)
		else:
			increment = self.increment
			increment_min = self.increment_min.format(min=increment_min)
			increment_max = self.increment_max.format(max=increment_max)
			attack = "{attack_mode} {masks} \"{wordlist}\" {rules_right} {increment} {increment_min} {increment_max}".format(attack_mode=attack_mode, wordlist=wordlist, rules_right=rules_right, masks=masks, increment=increment, increment_min=increment_min, increment_max=increment_max)
		cmd = self.getStaticPart() + attack
		self.execute(cmd)
		return

	def one_hash_one_word(self, one_hash, word):
		"""
		Call hashcat's brute force automatic attack: "hash" -a 3 "specific_word"
		"""
		attack_mode = self.attack_mode.format(mode=3)
		static = f"{self.executable} {self.hash_type} \"{one_hash}\" {self.pot_file} {self.out_file} {self.out_file_format_pwd} {self.resource_options} {self.extra_params} {self.quiet} "
		attack = "{attack_mode} {masks}".format(attack_mode=attack_mode, masks=word)
		cmd = static + attack
		self.execute(cmd)
		return

	def save_cracked(self):
		"""
		 Call hashcat's show command and save the cracked hashes from a given hashfile, hashtype and potfile
		"""
		cmd = f"{self.executable} {self.hash_type} \"{self.hash_file}\" {self.pot_file} {self.out_file_format_pwd} {self.extra_params} {self.show}"
		print(Color.cyan("\n" + cmd))
		f = open(self.out_file_cracked_path, 'w')
		p = subprocess.call(cmd, stdout=f, shell=True)
		f.close()
		print("Cracked hashes saved in " + self.out_file_cracked_path + " ...")
		return