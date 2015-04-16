import time
import json
import os

import config
import core.util.debug as debug

class LocalTerminal:

	def __init__(self, path):
		self.path = path
		
	
	def put(self, application, request, response):

		filename = '%s/%s.json'%(self.path, application)
		
		if os.path.exists(filename):
			stat = os.stat(filename)
			if stat.st_size > 1000000:
				os.remove(filename)


		with open(filename, 'a+') as f:
			data = {'request': request, 'response': response}
			f.write(json.dumps(data)+'\n')
			f.flush()

	def get(self, application):

		filename = '%s/%s.json'%(self.path, application)
		
		if os.path.exists(filename) == False:
			return []

		with open(filename, 'r') as f:
			data = f.read().split('\n')
			return data
