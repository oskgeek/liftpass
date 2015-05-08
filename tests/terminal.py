import unittest
import json
import requests
import sys
import string
import random

import config
import core.content.errors as errors
import core.api.main as main
import core.content.content as content
import core.util.extras as extras
import core.dashboard.terminal as terminal
from core.util.test import *


class TestTerminal(APITest):

	def testLog(self):

		backend = content.Content()
		a = backend.addApplication('Test SDK')
		
		jsonPricesA = backend.addPrices(a.key, 'JSON', json.dumps({'sword':1000}), None)
		jsonPricesB = backend.addPrices(a.key, 'JSON', json.dumps({'sword':2000}), None)
		
		backend.setABTest(a.key, {'groupAPrices_key': jsonPricesA.key})
		backend.setABTest(a.key, {'groupBPrices_key': jsonPricesB.key})
		
		data = {
			'user': '0'*32,
			'liftpass-debug': True,
			'events': [
				{
					'name': 'liftpass-metric',
					'progress': ['','','','','','','','']+[0]*32,
					'time': extras.unixTimestamp()
				}
			]
		}

		(status, b) = self.request('POST', '/sdk/update/v1/', data, application=a)

		theTerminal = terminal.getTerminal()

		res = theTerminal.get(a.key)

		self.assertEqual(len(res), 2)


suite = unittest.TestSuite()
suite.addTests(discoverTests(TestTerminal, config.APIServer['address'], config.APIServer['port'], config.UserKey, config.UserSecret, main.app))
unittest.TextTestRunner(verbosity=2).run(suite)
