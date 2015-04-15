import unittest
import json
import requests
import sys
import string
import random
import subprocess
import os
import signal
import time

import config
import core.content.errors as errors
import core.content.main as main
import core.content.content as content

from core.util.test import *
import core.util.extras as extras

def genRandomStrings(count, length):
	return map(lambda c: ''.join(map(lambda i: random.choice(string.ascii_uppercase), range(length))), range(count))

class TestApplication(APITest):

	def testAdd(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		self.assertEqual(a['name'], 'Test application')

	def testAddGet(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, b) = self.request('GET', '/applications/get/v1/', {'key': a['key']})
		self.assertEqual(a['name'], b['name'])
		self.assertEqual(a['key'], b['key'])
		self.assertEqual(a['created'], b['created'])

	def testAddDeleteGet(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, b) = self.request('DELETE', '/applications/delete/v1/', {'key': a['key']})
		self.assertEqual(b['deleted'], True)

	def testList(self):
		(status, a) = self.request('GET', '/applications/list/v1/', {})
		(status, b) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, c) = self.request('GET', '/applications/list/v1/', {})
		self.assertEqual(len(a['applications']), len(c['applications'])-1)
		for application in c['applications']:
			self.request('DELETE', '/applications/delete/v1/', {'key': application['key']})
		(status, d) = self.request('GET', '/applications/list/v1/', {})
		self.assertEqual(len(d['applications']), 0)
		
	def testUpdate(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, b) = self.request('PUT', '/applications/update/v1/', {'key': a['key'], 'name': 'The new name'})
		(status, c) = self.request('GET', '/applications/get/v1/', {'key': a['key']})
		self.assertEqual(c['name'], b['name'])

	# Get application with wrong key
	def testBadKey(self):
		(status, a) = self.request('GET', '/applications/get/v1/', {'key': ''})
		self.assertEqual(status, errors.ApplicationKeyDoesNotExist['status'])

	# Delete application with wrong key
	def testDeleteBadKey(self):
		(status, a) = self.request('DELETE', '/applications/delete/v1/', {'key': ''})
		self.assertEqual(status, errors.ApplicationKeyDoesNotExist['status'])

	# Update application with wrong key
	def testUpdateWithBadKey(self):
		(status, a) = self.request('PUT', '/applications/update/v1/', {'key': '', 'name': 'The new name'})
		self.assertEqual(status, errors.ApplicationKeyDoesNotExist['status'])


class TestCurrency(APITest):

	def testUpdateCurrency(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		
		values = genRandomStrings(8, 8)

		for i, v in enumerate(values):
			(status, b) = self.request('PUT', '/currencies/update/v1/', {'key': a['key'], 'currency%d'%(i+1):v})
		(status, c) = self.request('GET', '/currencies/get/v1/', {'key': a['key']})
		
		for i, v in enumerate(values):
			self.assertEqual(c['currency%d'%(i+1)], v)
		
	def testUpdateCurrencyWithBadKey(self):
		(status, c) = self.request('GET', '/currencies/get/v1/', {'key': ''})
		self.assertEqual(status, errors.ApplicationKeyDoesNotExist['status'])

class TestMetrics(APITest):

	def testUpdateMetrics(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		
		# Strings
		values = genRandomStrings(8, 8)
		for i, v in enumerate(values):
			(status, b) = self.request('PUT', '/metrics/update/v1/', {'key': a['key'], 'str%d'%(i+1):v})
		(status, c) = self.request('GET', '/metrics/get/v1/', {'key': a['key']})
		for i, v in enumerate(values):
			self.assertEqual(c['str%d'%(i+1)], v)
		
		# Numbers
		values = genRandomStrings(24, 8)
		for i, v in enumerate(values):
			(status, b) = self.request('PUT', '/metrics/update/v1/', {'key': a['key'], 'num%d'%(i+1):v})
		(status, c) = self.request('GET', '/metrics/get/v1/', {'key': a['key']})
		for i, v in enumerate(values):
			self.assertEqual(c['num%d'%(i+1)], v)	

	def testUpdateMetricsWithBadKey(self):
		(status, c) = self.request('GET', '/metrics/get/v1/', {'key': ''})
		self.assertEqual(status, errors.ApplicationKeyDoesNotExist['status'])

class TestGoods(APITest):

	def testAddAndGetGood(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, b) = self.request('POST', '/goods/add/v1/', {'key': a['key'], 'name':'Sword'})
		(status, c) = self.request('GET', '/goods/get/v1/', {'key': b['key']})
		self.assertEqual(b['name'], 'Sword')
		self.assertEqual(b['application_key'], a['key'])
		self.assertEqual(c['name'], b['name'])
		self.assertEqual(c['key'], b['key'])
		self.assertEqual(c['application_key'], b['application_key'])

	def testDeleteGood(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, b) = self.request('POST', '/goods/add/v1/', {'key': a['key'], 'name':'Sword'})
		(status, c) = self.request('DELETE', '/goods/delete/v1/', {'key': b['key']})

		self.assertEqual(c['deleted'], True)

	def testListGoods(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, b) = self.request('GET', '/goods/list/v1/', {'key': a['key']})
		(status, c) = self.request('POST', '/goods/add/v1/', {'key': a['key'], 'name':'Sword'})
		(status, d) = self.request('GET', '/goods/list/v1/', {'key': a['key']})
		self.assertEqual(len(b['goods']), len(d['goods'])-1)

	def testUpdateGood(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, b) = self.request('POST', '/goods/add/v1/', {'key': a['key'], 'name':'Sword'})
		(status, c) = self.request('PUT', '/goods/update/v1/', {'key': b['key'], 'name':'Sword 2'})

		self.assertEqual(c['name'], 'Sword 2')

	def testGetGoodWithBadKey(self):
		(status, c) = self.request('GET', '/goods/get/v1/', {'key': ''})
		self.assertEqual(status, errors.GoodKeyDoesNotExist['status'])

	def testGetApplicationGoodsWithBadKey(self):
		(status, c) = self.request('GET', '/goods/list/v1/', {'key': ''})
		self.assertEqual(len(c['goods']), 0)

class TestPrices(APITest):

	def testAddAndGetPrice(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, b) = self.request('POST', '/prices/add/v1/', {'key': a['key'], 'engine':'JSON', 'data':'{}', 'path':None})
		(status, c) = self.request('GET', '/prices/get/v1/', {'key': b['key']})

		self.assertEqual(b['engine'], 'JSON')
		self.assertEqual(b['application_key'], a['key'])
		self.assertEqual(b['data'], '{}')
		self.assertEqual(b['path'], None)

		self.assertEqual(b['engine'], c['engine'])
		self.assertEqual(b['application_key'],c['application_key'])
		self.assertEqual(b['data'], c['data'])
		self.assertEqual(b['path'], c['path'])

	def testDeletePrices(self):

		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, b) = self.request('POST', '/prices/add/v1/', {'key': a['key'], 'engine':'JSON', 'data':'{}', 'path':None})
		(statuc, c) = self.request('DELETE', '/prices/delete/v1/', {'key': b['key']})

		self.assertEqual(c['deleted'], True)

	def testListPrices(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, b) = self.request('GET', '/prices/list/v1/', {'key': a['key']})
		(status, c) = self.request('POST', '/prices/add/v1/', {'key': a['key'], 'engine':'JSON', 'data':'{}', 'path':None})
		(status, d) = self.request('GET', '/prices/list/v1/', {'key': a['key']})
		self.assertEqual(len(b['prices']), len(d['prices'])-1)

	def testGetPriceWithBadKey(self):
		(status, b) = self.request('GET', '/prices/get/v1/', {'key': ''})
		self.assertEqual(status, errors.PricesKeyDoesNotExist['status'])

class TestABTest(APITest):

	def testGetABTest(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, b) = self.request('GET', '/abtest/get/v1/', {'key': a['key']})

		self.assertEqual(b['application_key'], a['key'])
		self.assertEqual(b['dynamicPrices_key'], None)
		self.assertEqual(b['staticPrices_key'], None)
		self.assertEqual(b['countryWhiteList'], '')
		self.assertEqual(b['countryBlackList'], '')
		self.assertEqual(b['modulus'], 2)
		self.assertEqual(b['modulusLimit'], 0)

	def testUpdateABTest(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, b) = self.request('GET', '/abtest/get/v1/', {'key': a['key']})
		(status, c) = self.request('PUT', '/abtest/update/v1/', {'key': a['key'], 'countryWhiteList':'BR', 'countryBlackList':'PT', 'modulus': 6, 'modulusLimit': 3})

		self.assertEqual(c['application_key'], a['key'])
		self.assertEqual(c['dynamicPrices_key'], None)
		self.assertEqual(c['staticPrices_key'], None)
		self.assertEqual(c['countryWhiteList'], 'BR')
		self.assertEqual(c['countryBlackList'], 'PT')
		self.assertEqual(c['modulus'], 6)
		self.assertEqual(c['modulusLimit'], 3)

	def testUpdateABTestPrices(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, b) = self.request('POST', '/prices/add/v1/', {'key': a['key'], 'engine':'JSON', 'data':'{}', 'path':None})
		(status, c) = self.request('PUT', '/abtest/update/v1/', {'key': a['key'], 'dynamicPrices_key':b['key']})
		self.assertEqual(c['dynamicPrices_key'], b['key'])
	
	def testUpdateABTestBadPrices(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, b) = self.request('PUT', '/abtest/update/v1/', {'key': a['key'], 'dynamicPrices_key':'12134'})
		(status, c) = self.request('GET', '/abtest/get/v1/', {'key': a['key']})
		(status, d) = self.request('PUT', '/abtest/update/v1/', {'key': a['key'], 'staticPrices_key':'12134'})
		(status, e) = self.request('GET', '/abtest/get/v1/', {'key': a['key']})
		self.assertEqual(c['dynamicPrices_key'], None)
		self.assertEqual(e['staticPrices_key'], None)

	def testDeletePrices(self):
		(status, a) = self.request('POST', '/applications/add/v1/', {'name': 'Test application'})
		(status, b) = self.request('POST', '/prices/add/v1/', {'key': a['key'], 'engine':'JSON', 'data':'{}', 'path':None})
		(status, c) = self.request('PUT', '/abtest/update/v1/', {'key': a['key'], 'dynamicPrices_key':b['key']})
		(status, d) = self.request('GET', '/abtest/get/v1/', {'key': a['key']})
		(status, e) = self.request('DELETE', '/prices/delete/v1/', {'key': b['key']})
		(status, f) = self.request('GET', '/abtest/get/v1/', {'key': a['key']})

		# Fail to delete price when being used in an AB Test
		self.assertEqual(e['deleted'], 0)
		self.assertEqual(f['dynamicPrices_key'], b['key'])
		self.assertEqual(c['dynamicPrices_key'], b['key'])

		# Delete of price works when price not being used in an AB Test
		(status, g) = self.request('PUT', '/abtest/update/v1/', {'key': a['key'], 'dynamicPrices_key':None})
		self.assertEqual(g['dynamicPrices_key'], None)
		(status, h) = self.request('DELETE', '/prices/delete/v1/', {'key': b['key']})
		self.assertEqual(h['deleted'], True)

class TestSDK(APITest):

	def testCall(self):

		backend = content.Content()
		a = backend.addApplication('Test')
		
		jsonPricesA = backend.addPrices(a.key, 'JSON', json.dumps({'sword':1000}), None)
		jsonPricesB = backend.addPrices(a.key, 'JSON', json.dumps({'sword':2000}), None)
		
		backend.setABTest(a.key, {'dynamicPrices_key': jsonPricesA.key})
		backend.setABTest(a.key, {'staticPrices_key': jsonPricesB.key})
		
		data = {
			'user': '0'*32,
			'events': [
				{
					'name': 'gondola-metric',
					'progress': ['','','','','','','','']+[0]*24,
					'time': extras.unixTimestamp()
				}
			]
		}

		(status, b) = self.request('POST', '/update/v1/', data, application=a)
		self.assertEqual(b['sword'], 1000)

		data['user'] = '1'*32
		(status, c) = self.request('POST', '/update/v1/', data, application=a)
		self.assertEqual(c['sword'], 2000)
		

	def testCallWithMissingData(self):
		backend = content.Content()
		a = backend.addApplication('Test') 

		(status, b) = self.request('POST', '/update/v1/', {'user':'', 'events':[{}]}, application = a)
		self.assertEqual(status, errors.ApplicationUpdateIncomplete['status'])
		
		(status, c) = self.request('POST', '/update/v1/', {'events':[{}]}, application = a)
		self.assertEqual(status, errors.ApplicationUpdateIncomplete['status'])
		
		(status, d) = self.request('POST', '/update/v1/', {'user':''}, application = a)
		self.assertEqual(status, errors.ApplicationUpdateIncomplete['status'])

		(status, e) = self.request('POST', '/update/v1/', {'user':'', 'events':[]}, application = a)
		self.assertEqual(status, errors.ApplicationUpdateIncomplete['status'])

	def testCallWithBadKey(self):
		backend = content.Content()
		a = backend.addApplication('Test') 
		(status, a) = self.request('POST', '/update/v1/', {'user':'', 'events':[{}]}, application = a)
		self.assertEqual(status, errors.ApplicationUpdateIncomplete['status'])

# Start server
server = subprocess.Popen(['python3.4','%s/manage.py'%config.BasePath,'API','start'], preexec_fn=os.setsid, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2)

suite = unittest.TestSuite()

# Tests without testing server
suite.addTests(discoverTests(TestApplication, config.APIAddress, config.APIPort, config.UserKey, config.UserSecret, main.app))
suite.addTests(discoverTests(TestCurrency, config.APIAddress, config.APIPort, config.UserKey, config.UserSecret, main.app))
suite.addTests(discoverTests(TestMetrics, config.APIAddress, config.APIPort, config.UserKey, config.UserSecret, main.app))
suite.addTests(discoverTests(TestGoods, config.APIAddress, config.APIPort, config.UserKey, config.UserSecret, main.app))
suite.addTests(discoverTests(TestPrices, config.APIAddress, config.APIPort, config.UserKey, config.UserSecret, main.app))
suite.addTests(discoverTests(TestABTest, config.APIAddress, config.APIPort, config.UserKey, config.UserSecret, main.app))
suite.addTests(discoverTests(TestSDK, config.APIAddress, config.APIPort, config.UserKey, config.UserSecret, main.app))


# # Tests using server
suite.addTests(discoverTests(TestApplication, config.APIAddress, config.APIPort, config.UserKey, config.UserSecret))
suite.addTests(discoverTests(TestCurrency, config.APIAddress, config.APIPort, config.UserKey, config.UserSecret))
suite.addTests(discoverTests(TestMetrics, config.APIAddress, config.APIPort, config.UserKey, config.UserSecret))
suite.addTests(discoverTests(TestGoods, config.APIAddress, config.APIPort, config.UserKey, config.UserSecret))
suite.addTests(discoverTests(TestPrices, config.APIAddress, config.APIPort, config.UserKey, config.UserSecret))
suite.addTests(discoverTests(TestABTest, config.APIAddress, config.APIPort, config.UserKey, config.UserSecret))
suite.addTests(discoverTests(TestSDK, config.APIAddress, config.APIPort, config.UserKey, config.UserSecret))

unittest.TextTestRunner(verbosity=2).run(suite)

# Kill server
os.killpg(server.pid, signal.SIGTERM)