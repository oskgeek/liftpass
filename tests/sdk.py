import unittest
import json
import requests
import sys
import string
import random

import config
import service.sdk.main as main
import service.sdk.errors as errors

from util.test import *

from core import factory


class TestSDK(APITest):

	def testCall(self):

		content = factory.getContent()
		a = content.addGame('Test')
		
		jsonPricesA = content.addPrices(a.key, 'JSON', json.dumps({'sword':1000}), None)
		jsonPricesB = content.addPrices(a.key, 'JSON', json.dumps({'sword':2000}), None)
		
		content.setABTest(a.key, {'dynamicPrices_key': jsonPricesA.key})
		content.setABTest(a.key, {'staticPrices_key': jsonPricesB.key})
		
		data = {
			'application': a.key,
			'player': '0'*32,
			'events': [
				{
					'progress': ['','','','','','','','']+[0]*24,
				}
			]
		}

		(status, b) = self.request('POST', '/update/v1/', data)
		self.assertEqual(b['sword'], 1000)

		data['player'] = '1'*32
		(status, c) = self.request('POST', '/update/v1/', data)
		self.assertEqual(c['sword'], 2000)
		

	def testCallWithMissingData(self):
		(status, a) = self.request('POST', '/update/v1/', {'player':'', 'events':[{}]})
		self.assertEqual(status, errors.GameUpdateIncomplete['status'])
		
		(status, a) = self.request('POST', '/update/v1/', {'application':123, 'events':[{}]})
		self.assertEqual(status, errors.GameUpdateIncomplete['status'])
		
		(status, a) = self.request('POST', '/update/v1/', {'application':123, 'player':''})
		self.assertEqual(status, errors.GameUpdateIncomplete['status'])

		(status, a) = self.request('POST', '/update/v1/', {'application':123, 'player':'', 'events':[]})
		self.assertEqual(status, errors.GameUpdateIncomplete['status'])

	def testCallWithBadKey(self):
		(status, a) = self.request('POST', '/update/v1/', {'application':123, 'player':'', 'events':[{}]})
		self.assertEqual(status, errors.GameUpdateIncomplete['status'])

suite = unittest.TestSuite()
suite.addTests(discoverTests(TestSDK, config.SDKAddress, config.SDKPort, main.app))
unittest.TextTestRunner(verbosity=2).run(suite)
