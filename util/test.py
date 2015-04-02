import unittest
import requests
import json
import traceback

import util.debug as debug

def discoverTests(testcase, *args):

	res = []
	for f in dir(testcase):
		if 'test' in f and f.index('test') == 0:
			parameters = [f]+list(args)
			res.append(testcase(*parameters))
	return res

class APITest(unittest.TestCase):

	def __init__(self, f, address, port, flask = None):
		unittest.TestCase.__init__(self, f)
		
		if flask: 
			self.client = flask.test_client()
		else:
			self.client = None
		
		self.address = address
		self.port = port
		

	def request(self, method, url, data):
		address = 'http://%s:%d%s'%(self.address, self.port, url)

		if self.client: 
			try:
				if method == 'POST':
					result = self.client.post(address, data=json.dumps(data), content_type='application/json')
				elif method == 'GET':
					result = self.client.get(address, data=json.dumps(data), content_type='application/json')
				elif method == 'DELETE':
					result = self.client.delete(address, data=json.dumps(data), content_type='application/json')
				elif method == 'PUT':
					result = self.client.put(address, data=json.dumps(data), content_type='application/json')
				return (result.status_code, json.loads(result.data.decode("utf-8")))
			except Exception as e:
				debug.error('-'*60)
				debug.error(str(e))
				for line in traceback.format_stack():
					debug.error(line.replace('\n',''))
				debug.error('-'*60)
				return (500, {'error': 'Internal server error'})
		else:
			if method == 'POST':
				result = requests.post(address, json=data)
			elif method == 'GET':
				result = requests.get(address, json=data)
			elif method == 'DELETE':
				result = requests.delete(address, json=data)
			elif method == 'PUT':
				result = requests.put(address, json=data)
			return (result.status_code, json.loads(result.content.decode("utf-8")))