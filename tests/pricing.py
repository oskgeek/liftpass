import unittest
import json
import requests
import sys
import string
import random

import config
import core.content.errors as errors
import core.content.main as main
import core.content.content as content
import core.pricing.pricing as pricing

from core.util.test import *

class TestPricingEngine(unittest.TestCase):


	def testLoadEmptyPrices(self):
		backend = content.Content()
		a = backend.addGame('Test')
		p = pricing.PricingEngine(a.key)

		self.assertEqual(p.dynamicPrices, None)
		self.assertEqual(p.staticPrices, None)


	def testLoadPrices(self):
		backend = content.Content()
		a = backend.addGame('Test')
		
		jsonPrices = backend.addPrices(a.key, 'JSON', json.dumps({'sword':1000}), None)

		backend.setABTest(a.key, {'dynamicPrices_key': jsonPrices.key})

		p = pricing.PricingEngine(a.key)

		self.assertNotEqual(p.dynamicPrices, None)
		self.assertEqual(p.staticPrices, None)


	def testPricesWithProgress(self):
		backend = content.Content()
		a = backend.addGame('Test')
		
		jsonPricesA = backend.addPrices(a.key, 'JSON', json.dumps({'sword':1000}), None)
		jsonPricesB = backend.addPrices(a.key, 'JSON', json.dumps({'sword':2000}), None)

		backend.setABTest(a.key, {'dynamicPrices_key': jsonPricesA.key})
		backend.setABTest(a.key, {'staticPrices_key': jsonPricesB.key})

		pricing = backend.getPricingEngine(a.key)
		
		pricesA = pricing.getPrices('a', [0]*32)
		pricesB = pricing.getPrices('b', [0]*32)

		self.assertEqual(pricesA['sword'], 1000)
		self.assertEqual(pricesB['sword'], 2000)
		

	def testPricesWithBadGameKey(self):
		backend = content.Content()
		with self.assertRaises(pricing.GameNotFoundException):
			gamePrices = backend.getPricingEngine('12345')
		
		

suite = unittest.TestSuite()
suite.addTests(discoverTests(TestPricingEngine))
unittest.TextTestRunner(verbosity=2).run(suite)


