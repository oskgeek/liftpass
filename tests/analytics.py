import unittest
import json
import requests
import sys
import string
import random
import datetime

from core.util.test import *
import core.util.extras as extras
import core.analytics.analytics as analytics

class TestUpdate(unittest.TestCase):

	def testNormalUpdate(self):
		update = {
			'name': 'gondola-metric',
			'progress': [],
			'time': extras.unixTimestamp(),
		}

		for i in range(8):
			update['progress'].append(extras.genRandomStrings(1, 12)[0])
		for i in range(24):
			update['progress'].append(random.random())

		event = analytics.Analytics().processEvent(update)

		self.assertEqual(event.name, update['name'])
		self.assertEqual(event.timestamp, datetime.datetime.utcfromtimestamp(update['time']))
		
		for i in range(8):
			self.assertEqual(getattr(event, 'metricString%d'%(i+1)), update['progress'][i])
		for i in range(24):
			self.assertEqual(getattr(event, 'metricNumber%d'%(i+1)), update['progress'][8+i])

	def testNullMetrics(self):
		update = {
			'name': 'gondola-metric',
			'progress': [None]*32,
			'time': extras.unixTimestamp(),
		}
		event = analytics.Analytics().processEvent(update)
		for i in range(8):
			self.assertEqual(getattr(event, 'metricString%d'%(i+1)), update['progress'][i])
		for i in range(24):
			self.assertEqual(getattr(event, 'metricNumber%d'%(i+1)), update['progress'][8+i])

	def testMissingEventMetrics(self):
		update = {
			'name': 'gondola-metric',
			'progress': [None]*23,
			'time': extras.unixTimestamp(),
		}
		with self.assertRaises(analytics.EventMissingMetricError):
			event = analytics.Analytics().processEvent(update)

		update = {
			'name': 'gondola-metric',
			'time': extras.unixTimestamp(),
		}
		with self.assertRaises(analytics.EventAttributeMissingError):
			event = analytics.Analytics().processEvent(update)

	def testMissingEventTime(self):
		update = {
			'name': 'gondola-metric',
			'progress': [None]*23,
		}
		with self.assertRaises(analytics.EventAttributeMissingError):
			event = analytics.Analytics().processEvent(update)

	def testMissingEventName(self):
		update = {
			'progress': [None]*23,
			'time': extras.unixTimestamp(),
		}
		with self.assertRaises(analytics.EventAttributeMissingError):
			event = analytics.Analytics().processEvent(update)

	def testMissingAttribute(self):
		update = {
			'name': 'gondola-metric',
			'progress': [None]*32,
			'attributes': [None]*12,
			'time': extras.unixTimestamp(),
		}
		with self.assertRaises(analytics.EventMissingAttributeError):
			event = analytics.Analytics().processEvent(update)



suite = unittest.TestSuite()
suite.addTests(discoverTests(TestUpdate))
unittest.TextTestRunner(verbosity=2).run(suite)
