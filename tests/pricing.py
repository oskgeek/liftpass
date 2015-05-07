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
import core.pricing.pricing as pricing

from core.util.test import *

class TestPricingEngine(unittest.TestCase):


	def testLoadEmptyPrices(self):
		backend = content.Content()
		a = backend.addApplication('Test')
		p = pricing.PricingEngine(a.key)

		self.assertEqual(p.groupAPrices, None)
		self.assertEqual(p.groupBPrices, None)


	def testLoadPrices(self):
		backend = content.Content()
		a = backend.addApplication('Test')
		
		jsonPrices = backend.addPrices(a.key, 'JSON', json.dumps({'sword':1000}), None)

		backend.setABTest(a.key, {'groupAPrices_key': jsonPrices.key})

		p = pricing.PricingEngine(a.key)

		self.assertNotEqual(p.groupAPrices, None)
		self.assertEqual(p.groupBPrices, None)


	def testPricesWithProgress(self):
		backend = content.Content()
		a = backend.addApplication('Test')
		
		jsonPricesA = backend.addPrices(a.key, 'JSON', json.dumps({'sword':1000}), None)
		jsonPricesB = backend.addPrices(a.key, 'JSON', json.dumps({'sword':2000}), None)

		backend.setABTest(a.key, {'groupAPrices_key': jsonPricesA.key})
		backend.setABTest(a.key, {'groupBPrices_key': jsonPricesB.key})

		pricing = backend.getPricingEngine(a.key)
		
		pricesA = pricing.getPrices('a', [0]*32)
		pricesB = pricing.getPrices('b', [0]*32)
		
		self.assertEqual(pricesA['sword'][0], 1000)
		self.assertEqual(pricesB['sword'][0], 2000)
		

	def testPricesWithBadApplicationKey(self):
		backend = content.Content()
		with self.assertRaises(pricing.ApplicationNotFoundException):
			applicationPrices = backend.getPricingEngine('12345')
		
class TestJSONEngine(unittest.TestCase):		
	def testEngine(self):
		p = pricing.JSONDataEngine.validate({'data': json.dumps({'sword':1000})})
		self.assertIsInstance(p, dict)

		p = pricing.JSONDataEngine.validate({'data': json.dumps({'sword':[1000]})})
		self.assertIsInstance(p, dict)

		with self.assertRaises(pricing.DataEngineException):
			p = pricing.JSONDataEngine.validate({'data': json.dumps({'sword':'1000'})})
		
		with self.assertRaises(pricing.DataEngineException):
			p = pricing.JSONDataEngine.validate({'data': json.dumps({'sword':[1,2,3,4,5,6,7,8,9]})})
		
		with self.assertRaises(pricing.DataEngineException):
			p = pricing.JSONDataEngine.validate({'data': json.dumps({'sword':[1,2,3,'4',5,6,7,8,9]})})
	



class TestCSVEngine(unittest.TestCase):

	def testEngine(self):
		data = """
			sword, 1000
			saber, 2000
			knife, 500
		"""	
		p = pricing.CSVDataEngine.validate({'data': data})
		self.assertIsInstance(p, dict)

		data = """
			sword, 1000, 300
			saber, 2000, 400
			knife, 500
		"""	
		with self.assertRaises(pricing.DataEngineException):
			p = pricing.CSVDataEngine.validate({'data': data})
		data = """
			sword,
			saber, 2000, 400
			knife, 500
		"""	
		with self.assertRaises(pricing.DataEngineException):
			p = pricing.CSVDataEngine.validate({'data': data})
		data = """
			sword, "100"
			saber, 2000, 400
			knife, 500
		"""	
		with self.assertRaises(pricing.DataEngineException):
			p = pricing.CSVDataEngine.validate({'data': data})

class TestMetricCSVEngine(unittest.TestCase):

	def testEngine(self):

		data = """
			metricString5, Default, US, BR, DE
			sword, 100, 200, 300, 500
			saber, 200, 300, 400, 600
			knife, 300, 400, 500, 700

		"""
		p = pricing.MetricCSVDataEngine.validate({'data':data})
		self.assertEqual(p['data']['Default']['sword'][0], 100)
		self.assertEqual(p['data']['Default']['knife'][0], 300)
		self.assertEqual(p['data']['US']['sword'][0], 200)
		self.assertEqual(p['data']['US']['knife'][0], 400)
		self.assertEqual(p['data']['DE']['sword'][0], 500)
		self.assertEqual(p['data']['DE']['knife'][0], 700)
		self.assertEqual(p['metric'], 4)

		# Check number metric conversion 
		data = """
			metricNumber5, Default, US, BR, DE
			sword, 100, 200, 300, 500
		"""
		p = pricing.MetricCSVDataEngine.validate({'data':data})
		self.assertEqual(p['metric'], 12)

		# Metric number out of bound
		data = """
			metricNumber40, Default, US, BR, DE
			sword, 100, 200, 300, 500
		"""
		with self.assertRaises(pricing.DataEngineException):
			p = pricing.MetricCSVDataEngine.validate({'data':data})
		
		# Unrecognized metric
		data = """
			something12, Default, US, BR, DE
			sword, 100, 200, 300, 500
		"""
		with self.assertRaises(pricing.DataEngineException):
			p = pricing.MetricCSVDataEngine.validate({'data':data})

		# Row with missing column
		data = """
			metricNumber5, Default, US, BR, DE
			sword, 100, 200, 300
		"""
		with self.assertRaises(pricing.DataEngineException):
			p = pricing.MetricCSVDataEngine.validate({'data':data})

		# Row with too many elements
		data = """
			metricNumber5, Default, US, BR, DE
			sword, 100, 200, 300, 400, 500
		"""
		with self.assertRaises(pricing.DataEngineException):
			p = pricing.MetricCSVDataEngine.validate({'data':data})

		# Row with wrong type of value
		data = """
			metricNumber5, Default, US, BR, DE
			sword, 100, 200, 'abc', 400, 500
		"""
		with self.assertRaises(pricing.DataEngineException):
			p = pricing.MetricCSVDataEngine.validate({'data':data})






suite = unittest.TestSuite()
suite.addTests(discoverTests(TestPricingEngine))
suite.addTests(discoverTests(TestCSVEngine))
suite.addTests(discoverTests(TestJSONEngine))
suite.addTests(discoverTests(TestMetricCSVEngine))

unittest.TextTestRunner(verbosity=2).run(suite)


