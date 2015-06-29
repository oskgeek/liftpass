import unittest
import requests
import json
import traceback
import time
import hashlib
import hmac
import string
import base64
import sys
import io

import core.util.debug as debug

def discoverTests(testcase, *args):

	res = []
	for f in dir(testcase):
		if 'test' in f and f.index('test') == 0:
			parameters = [f]+list(args)
			res.append(testcase(*parameters))
	return res

class APITest(unittest.TestCase):

	def __init__(self, f, address, port, userKey, userSecret, client = None):
		unittest.TestCase.__init__(self, f)
		
		if client: 
			self.client = client.test_client()
		else:
			self.client = None
		
		self.address = address
		self.port = port
		self.userKey = userKey
		self.userSecret = userSecret
		

	def request(self, method, url, data, application=None, raw=False, forceNetwork=False):
		address = 'http://%s:%d%s'%(self.address, self.port, url)

		if application:
			data['liftpass-application'] = application.key
			self.userSecret = application.secret.encode('utf-8')
		else:	
			data['liftpass-user'] = self.userKey.decode('utf-8')
		
		data['liftpass-time'] = round(time.time())
		data['liftpass-url'] = url

		dump = json.dumps(data).encode('utf-8')
		digest = hmac.new(self.userSecret, dump, hashlib.sha256).hexdigest()
		header = {'liftpass-hash': digest}
		
		try:
			if self.client and forceNetwork == False: 
				if method == 'POST':
					result = self.client.post(address, data=json.dumps(data), headers=header, content_type='application/json')
				elif method == 'GET':
					result = self.client.get(address, data=json.dumps(data), headers=header, content_type='application/json')
				elif method == 'DELETE':
					result = self.client.delete(address, data=json.dumps(data), headers=header, content_type='application/json')
				elif method == 'PUT':
					result = self.client.put(address, data=json.dumps(data), headers=header, content_type='application/json')

				if len(result.data) == 0:
					return (result.status_code, None)

				if raw == True:
					data = result.data.decode("utf-8")
				else: 
					data = json.loads(result.data.decode("utf-8"))
					
				return (result.status_code, data)			
			else:
				if method == 'POST':
					result = requests.post(address, json=data, headers=header, timeout=1.0)
				elif method == 'GET':
					result = requests.get(address, json=data, headers=header, timeout=1.0)
				elif method == 'DELETE':
					result = requests.delete(address, json=data, headers=header, timeout=1.0)
				elif method == 'PUT':
					result = requests.put(address, json=data, headers=header, timeout=1.0)
				
				if len(result.content) == 0:
					return (result.status_code, None)
				
				if raw == True:
					data = result.content.decode('utf-8')
				else:
					data = result.content.decode('utf-8')
					data = json.loads(data)
				
				return (result.status_code, data)
		except Exception as e:
				debug.stacktrace(e)
				return (500, {'message': 'Internal server error'})