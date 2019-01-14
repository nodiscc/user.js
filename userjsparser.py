#!/usr/bin/python3

import sys
import re

class UserjsSyntaxError(Exception):
	"""docstring for UserjsSyntaxError"""
	def __init__(self, arg):
		super(UserjsSyntaxError, self).__init__()
		self.arg = arg

		

with open(sys.argv[1]) as inputfile:
	paragraphs = re.split('\n\n',inputfile.read())
	for paragraph in paragraphs:
		pref_descriptions = re.findall('^// PREF.*', paragraph)
		notices = re.findall('\n// NOTICE.*', paragraph)
		info_urls = re.findall('\n// http.*', paragraph)
		user_prefs = re.findall('\nuser_pref.*', paragraph)
		disabled_user_prefs = re.findall('// user_pref.*', paragraph)
		
		if len(pref_descriptions) > 1:
			raise UserjsSyntaxError("Entry has more than one description line")
		elif len(pref_descriptions) == 0:
			continue
		else:
			pref_description = pref_descriptions[0].replace('// PREF: ', '')
			print('Pref description: {}'.format(pref_description))

		if len(disabled_user_prefs) > 0:
			state = 'disabled'
		else:
			state = 'enabled'
		print('State: {}'.format(state))

		if len(notices) == 0:
			pass
		else:
			for notice in notices:
				print('NOTICE: {}'.format(notice.replace('\n// NOTICE: ', '')))

		if len(info_urls) == 0:
			pass
		else:
			for info_url in info_urls:
				print('Info URL: {}'.format(info_url.replace('\n// ', '')))

		if len(disabled_user_prefs) > 0 and len(user_prefs) > 0:
			raise UserjsSyntaxError("Entry has both enabled and disabled prefs!")
		else:
			for user_pref in user_prefs + disabled_user_prefs:
				setting = re.findall('user_pref\((.*)\);', user_pref)
				data = setting[0].replace('\t', '').split(',', 1)
				pref_name = data[0]
				pref_value = data[1]
				print('Name: {}, Value: {}'.format(pref_name, pref_value))

		print('\n')
