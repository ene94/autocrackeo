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
		self.out_file_cracked_path = conf["out_file_cracked"]
		self.hash_file_path = conf["hash_file"]
		self.hash_type = conf["hash_type"]
		self.config_file_path = conf["config_file"]

		# calculate data
		self.hashes_total = self.count_lines(self.hash_file_path)
		self.cracked_total = -1

	def get_summary(self):
		self.percentage_total = "{:.2%}".format(self.cracked_total/self.hashes_total)
		report = '''
		RESULTS:

		hash type:\t\t{hash_type}
		hash file:\t\t{hash_file_path}
		cracked outfile:\t{out_file_cracked_path}

		hashes total:\t\t{hashes_total}
		cracked total:\t\t{cracked_total}  ({percentage_total})
		'''.format(hash_type=self.hash_type, hash_file_path=self.hash_file_path,
			out_file_cracked_path=self.out_file_cracked_path,
			hashes_total=self.hashes_total,
			cracked_total=self.cracked_total, percentage_total=self.percentage_total)

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