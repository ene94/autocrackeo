# -*- coding: utf-8 -*-
try:
	import sys, json
	from src.color import Color
	from datetime import datetime, timedelta
except Exception as e:
	sys.exit(e)



class Results(object):
	"""
	Analyze and calculate a summary of the results of hashcat executions
	"""
	def __init__(self, conf):
		# get info
		#self.report_file_path = conf["report_file"]
		self.out_file_cracked_path = conf["out_file_cracked"]
		self.out_file_left_path = conf["out_file_left"]
		self.out_file_path = conf["out_file"]
		self.hash_file_path = conf["hash_file"]
		self.hash_type = conf["hash_type"]
		self.config_file_path = conf["config_file"]

		# calculate data
		self.start_date = datetime.now()
		self.end_date = None
		self.duration = None
		self.hashes_total = self.count_lines(self.hash_file_path)
		self.cracked_total = -1
		self.hashes_left = -1
		self.attacks = []

		# generate if doesn't exist
		open(self.out_file_path, 'a').close()
		
		# generate if doesn't exist and follow
		self.out_file = open(self.out_file_path, "r", encoding="utf-8")
		self.out_file.seek(0,2) # move to the end of the file
		

	def get_last_cracked(self):
		lines = self.out_file.read().splitlines()
		return lines

	def save_attack(self, cmd):
		last_cracked = self.get_last_cracked()
		if len(last_cracked) > 0:
			print(Color.green("\t".join(last_cracked)))
		last_cracked_string = " ".join(last_cracked)
		if cmd:
			self.attacks.append([cmd, len(last_cracked), last_cracked_string])
		return

	def get_summary(self):
		self.end_date = datetime.now()
		self.duration = self.end_date - self.start_date
		self.percentage_total = "{:.2%}".format(self.cracked_total/self.hashes_total)
		self.percentage_left = "{:.2%}".format(self.cracked_left/self.hashes_total)
		report = '''
		RESULTS:

		hash type:\t\t\t\t{hash_type}
		hash file:\t\t\t\t{hash_file_path}
		config file:\t\t\t\t{config_file_path}
		cracked hashes:\t\t\t\t{out_file_cracked_path}
		hashes left to crack:\t\t\t{out_file_left_path}
		plaintext passwords:\t\t\t{out_file_path}

		start date:\t\t\t\t{start_date}
		end date:\t\t\t\t{end_date}
		duration:\t\t\t\t{duration}

		hashes total:\t\t\t\t{hashes_total}
		cracked total:\t\t\t\t{cracked_total}  ({percentage_total})
		hashes left:\t\t\t\t{cracked_left}  ({percentage_left})
		'''.format(hash_type=self.hash_type, hash_file_path=self.hash_file_path, 
			config_file_path=self.config_file_path, out_file_path=self.out_file_path,
			out_file_cracked_path=self.out_file_cracked_path, out_file_left_path=self.out_file_left_path,
			start_date=Results.datetime_to_string(self.start_date),
			end_date=Results.datetime_to_string(self.end_date), 
			duration=Results.timedelta_to_string(self.duration),
			hashes_total=self.hashes_total,
			cracked_total=self.cracked_total, percentage_total=self.percentage_total,
			cracked_left=self.cracked_left, percentage_left=self.percentage_left)

		return report

	@staticmethod
	def count_lines(file_path):
			try:
				f = open(file_path, "r")
				count = len(f.readlines())
				f.close()
				return count
			except Exception as e:
				f.close()
				Color.show_error(str(e))
				return -1

	@staticmethod
	def string_to_datetime(date_time_string):
		fmt = '%d/%m/%Y %H:%M:%S' # ex. 04012011172008 <- Jan. 04, 2011 5:20:08pm 
		date_time = datetime.strptime(date_time_string, fmt)
		return date_time
		
	@staticmethod
	def datetime_to_string(date_time):
		fmt = '%d/%m/%Y %H:%M:%S' # ex. 20110104172008 -> Jan. 04, 2011 5:20:08pm 
		date_time_string = date_time.strftime(fmt)
		return date_time_string

	@staticmethod
	def timedelta_to_string(time_delta):
		td = str(time_delta).split('.')[0]
		td = td.split(':')
		return "{0}h {1}m {2}s".format(td[0], td[1], td[2])

	@staticmethod
	def datetime_converter(obj):
		if isinstance(obj, datetime):
			return Results.datetime_to_string(obj)
		if isinstance(obj, timedelta):
			return Results.timedelta_to_string(obj)

'''
	def generate_report(self):
		dictionary = self.__dict__
		json_data = {} # 2 fields: attacks and summary
		json_data["attacks"] = dictionary.pop("attacks") # individual results
		json_data["summary"] = dictionary # generic results
		json_data["summary"].pop("out_file")

		# write results
		with open(self.report_file_path, 'w') as out_file:
			out_file.seek(0, 2)
			json.dump(json_data, out_file, default=Results.datetime_converter, indent=4, separators=(',', ': '), sort_keys = True)
		return
'''