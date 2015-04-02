import unittest
import json
import requests
import sys
import string
import random

import config
import service.api.errors as errors
import service.api.main as main
import engine.pricing.pricing as pricing

from util.test import *

from core import factory

class TestPricingEngine(unittest.TestCase):

	def testLoadEmptyPrices(self):
		content = factory.getContent()
		a = content.addGame('Test')
		p = pricing.PricingEngine(a.key)

		self.assertEqual(p.dynamicPrices, None)
		self.assertEqual(p.staticPrices, None)

	def testLoadPrices(self):
		content = factory.getContent()
		a = content.addGame('Test')
		
		jsonPrices = content.addPrices(a.key, 'JSON', json.dumps({'sword':1000}), None)

		content.setABTest(a.key, {'dynamicPrices_key': jsonPrices.key})

		p = pricing.PricingEngine(a.key)

		self.assertNotEqual(p.dynamicPrices, None)
		self.assertEqual(p.staticPrices, None)

	def testPricesWithProgress(self):
		content = factory.getContent()
		a = content.addGame('Test')
		
		jsonPricesA = content.addPrices(a.key, 'JSON', json.dumps({'sword':1000}), None)
		jsonPricesB = content.addPrices(a.key, 'JSON', json.dumps({'sword':2000}), None)

		content.setABTest(a.key, {'dynamicPrices_key': jsonPricesA.key})
		content.setABTest(a.key, {'staticPrices_key': jsonPricesB.key})

		pricing = content.getPricingEngine(a.key)
		
		pricesA = pricing.getPrices('a', [0]*32)
		pricesB = pricing.getPrices('b', [0]*32)

		self.assertEqual(pricesA['sword'], 1000)
		self.assertEqual(pricesB['sword'], 2000)
		
	def testPricesWithBadGameKey(self):

		content = factory.getContent()
		pricing = content.getPricingEngine('12345')

		pricesA = pricing.getPrices('a', [0]*32)
		pricesB = pricing.getPrices('b', [0]*32)

		self.assertEqual(pricesA, None)
		self.assertEqual(pricesB, None)
		

suite = unittest.TestSuite()
suite.addTests(discoverTests(TestPricingEngine))
unittest.TextTestRunner(verbosity=2).run(suite)


