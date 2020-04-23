# -*- coding: utf-8 -*-
try:
	import sys
	from src.color import Color
except Exception as e:
	sys.exit(e)

class Attacks():

	"""
	 Parse attacks config data
	 For every attack call to hashcat method
	 [all_hashes]:[specified_wordlists]
	"""

	def __init__(self, hashcat):
		self.hashcat = hashcat

	@staticmethod
	def get_file_from_index(indexes, all_files):
		"""
		Get selected items giving two arrays:
			indexes: array with the selected item's indexes
			all_files: array with all files available to select
		"""
		if len(indexes) == 0: # if not defined
			files = all_files # take every file
		else: 
			files = []
			for i in indexes: # take just selected index files
				files.append(all_files[i])
		return files

	def straight_attacks(self, attack_name, attacks, all_wordlists, all_rules):
		"""
		Parse configuration's STRAIGHT attack parameters and call the corresponding hashcat class method
		"""
		for attack in attacks: # for every attack
			wordlists = Attacks.get_file_from_index(attack["wordlists"], all_wordlists)
			if "rules" in attack:
				if attack_name == "straight_with_rules_manual":
					r = attack["rules"]
				else:
					rules = Attacks.get_file_from_index(attack["rules"], all_rules)

			for w in wordlists: # for every wordlist
				if attack_name == "straight":
					self.hashcat.straight(w)
				elif attack_name == "straight_with_combined_rules_files":
					if len(rules) == 2: # only if 2 rule files are given
						self.hashcat.straight_with_combined_rules_files(w, rules[0], rules[1])
					else:
						Color.showError("Straight combined rules: You have to define two rule files!", False)
				elif attack_name == "straight_with_rules_manual":
							self.hashcat.straight_with_rules_manual(w, r)
				elif attack_name == "straight_with_rules_files":
					for r in rules: # apply all the defined rules
						self.hashcat.straight_with_rules_file(w, r)
		return

	def combinator_attacks(self, attack_name, attacks, all_wordlists):
		"""
		Parse configuration's COMBINATOR attack parameters and call the corresponding hashcat class method
		"""
		for attack in attacks: # for every attack
			wordlists = Attacks.get_file_from_index(attack["wordlists"], all_wordlists)
			if len(wordlists) == 2: # only if 2 wordlists are given
				w1 = wordlists[0]
				w2 = wordlists[1]
				if attack_name == "combinator":
					self.hashcat.combinator(w1, w2)
				elif attack_name == "":
					j = attack["rules_left"]
					k = attack["rules_right"]
					self.hashcat.combinator(w1, w2, j, k)
			else:
				Color.showError("Combined rules: You have to define two rule files!", False)
		return

	def brute_force_attacks(self, attack_name, attacks, all_masks):
		"""
		Parse configuration's BRUTE FORCE attack parameters and call the corresponding hashcat class method
		"""
		for attack in attacks: # for every attack
			if attack_name == "brute_force_with_masks_manual":
				m = attack["masks"]
			elif attack_name == "brute_force_with_masks_files":
				masks = Attacks.get_file_from_index(attack["masks"], all_masks)

			if attack["increment_enable"] == True: # only if increment is enabled
				increment_min = attack["increment_min"]
				increment_max = attack["increment_max"]
				if attack_name == "brute_force_automatic":
					self.hashcat.brute_force_automatic(increment_min, increment_max)
				elif attack_name == "brute_force_with_masks_manual":
					self.hashcat.brute_force(m, increment_min, increment_max)
				elif attack_name == "brute_force_with_masks_files":
					for m in masks:
						self.hashcat.brute_force(m, increment_min, increment_max)
			else:
				if attack_name == "brute_force_automatic":
					self.hashcat.brute_force_automatic()
				elif attack_name == "brute_force_with_masks_manual":
					self.hashcat.brute_force(m)
				elif attack_name == "brute_force_with_masks_files":
					for m in masks:
						self.hashcat.brute_force(m)
		return

	def hybrid_attacks(self, attack_name, attacks, all_wordlists, all_masks):
		"""
		Parse configuration's HYBRID attack parameters and call the corresponding hashcat class method
		"""
		for attack in attacks: # for every attack
			# parse params
			wordlists = Attacks.get_file_from_index(attack["wordlists"], all_wordlists)
			if "rules_left" in attack:
				j = attack["rules_left"]
			if "rules_right" in attack:
				k = attack["rules_right"]
			if attack_name == "hybrid_right_with_masks_files" or attack_name == "hybrid_left_with_masks_files":
				masks = Attacks.get_file_from_index(attack["masks"], all_masks)
			elif attack_name == "hybrid_right_with_masks_manual" or attack_name == "hybrid_left_with_masks_manual":
				m = attack["masks"]

			for w in wordlists: # for every wordlist
				if attack["increment_enable"] == True: # only if increment is enabled
						increment_min = attack["increment_min"]
						increment_max = attack["increment_max"]
						if attack_name == "hybrid_right_with_masks_manual":
							self.hashcat.hybrid_right(w, m, j, increment_min, increment_max)
						elif attack_name == "hybrid_left_with_masks_manual":
							self.hashcat.hybrid_left(w, m, k, increment_min, increment_max)
						else:
							for m in masks:
								if attack_name == "hybrid_right_with_masks_files":
									self.hashcat.hybrid_right(w, m, j, increment_min, increment_max)
								elif attack_name == "hybrid_left_with_masks_files":
									self.hashcat.hybrid_left(w, m, k, increment_min, increment_max)
				else:
					if attack_name == "hybrid_right_with_masks_manual":
						self.hashcat.hybrid_right(w, m, j)
					elif attack_name == "hybrid_left_with_masks_manual":
						self.hashcat.hybrid_left(w, m, k)
					else:
						for m in masks:
							if attack_name == "hybrid_right_with_masks_files":
								self.hashcat.hybrid_right(w, m, j)
							elif attack_name == "hybrid_left_with_masks_files":
								self.hashcat.hybrid_left(w, m, k)
		return

	"""
	 Quick ugly fix to execute just "one different word" for every hash,
	 instead of "whole wordlist" for every hash
	"""
	def OneWordPerHashAttacks(self, attack_name, attacks, all_wordlists):
		"""
		Parse configuration's ONE WORD PER HASH attack parameters and call the corresponding hashcat class method
		One_hash:one_word line by line from hashlist:wordlist
		Note: useful to try username as the password
		"""
		for attack in attacks: # for every attack
			f = open(self.hashcat.hash_file, "r")
			hash_lines = f.read().splitlines() # get haslist
			f.close()
			wordlists = Attacks.get_file_from_index(attack["wordlists"], all_wordlists) # get wordlists

			for wordlist in wordlists: # for every wordlist
				f = open(wordlist, "r")
				word_lines = f.read().splitlines() # get wordlist
				f.close()

				if len(hash_lines) == len(word_lines):
					for i in range(len(hash_lines)):
						one_hash = hash_lines[i]
						one_word = word_lines[i] # its line corresponding hash:word
						self.hashcat.one_hash_one_word(one_hash,one_word)
				else:
					Color.showError("Hash file and Wordlist file need same length to try hash[i]:word[i]", True)
		return