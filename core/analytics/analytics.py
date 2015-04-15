import json
import datetime


import core.storage as storage
import core.util.extras as extras
import core.util.debug as debug
import core.content.models as models

import config

class EventAttributeMissingError(Exception):
	def __init__(self, attribute):
		self.attribute = attribute

	def __str__(self):
		return 'Event missing attribute "%s"'%self.attribute

class EventProgressMetricFormatError(Exception):
	def __str__(self):
		return 'Event metric is not correct data type'

class EventAttributeFormatError(Exception):
	def __str__(self):
		return 'Event attribute is not correct data type'

class EventTimestampError(Exception):
	def __str__(self):
		return 'Event timestamp is invalid'

class EventMissingMetricError(Exception):
	def __str__(self):
		return 'Event has wrong number of progress metrics'

class EventMissingAttributeError(Exception):
	def __str__(self):
		return 'Event has wrong number of attributes'

def checkString(x): 
	if x == None or type(x) == str:
		return x
	raise Exception()

def checkFloat(x):
	if x == None:
		return None
	elif type(float(x)) == float:
		return float(x)
	raise Exception()

class Analytics:
	def __init__(self):

		self.storage = storage.getStorage(config.AnalyticsStorage)



	def saveUpdate(self, update):
		key = '%s-%s-%s.json'%(update['gondola-application'], extras.datetimeStamp(), update['user'])
		self.storage.save(key, json.dumps(update))



	def processUpdate(self, filename):
		session = models.getSession()

		data = self.storage.load(filename)
		data = json.loads(data)

		if extras.keysInDict(data, ['gondola-ip', 'gondola-application', 'user', 'event']):
			debug.error('Failed to process update %s'%filename)
			return

		for update in data['events']:
			try:
				event = self.processEvent(update)
				session.add(event)
			except Exception as e:
				print(e)

		session.commit()



	def processEvent(self, data):
		if 'name' not in data:
			raise EventAttributeMissingError('name')
		if 'time' not in data:
			raise EventAttributeMissingError('name')
		if 'progress' not in data:
			raise EventAttributeMissingError('progress')
		if len(data['progress']) != 32:
			raise EventMissingMetricError()

		event = models.Events()
		event.name = data['name']
		try:
			event.timestamp = datetime.datetime.utcfromtimestamp(data['time'])
		except:
			raise EventTimestampError()

		# Try processing each progress metric
		try:
			event.metricString1 = checkString(data['progress'][0])
			event.metricString2 = checkString(data['progress'][1])
			event.metricString3 = checkString(data['progress'][2])
			event.metricString4 = checkString(data['progress'][3])
			event.metricString5 = checkString(data['progress'][4])
			event.metricString6 = checkString(data['progress'][5])
			event.metricString7 = checkString(data['progress'][6])
			event.metricString8 = checkString(data['progress'][7])
			event.metricNumber1 = checkFloat(data['progress'][8])
			event.metricNumber2 = checkFloat(data['progress'][9])
			event.metricNumber3 = checkFloat(data['progress'][10])
			event.metricNumber4 = checkFloat(data['progress'][11])
			event.metricNumber5 = checkFloat(data['progress'][12])
			event.metricNumber6 = checkFloat(data['progress'][13])
			event.metricNumber7 = checkFloat(data['progress'][14])
			event.metricNumber8 = checkFloat(data['progress'][15])
			event.metricNumber9 = checkFloat(data['progress'][16])
			event.metricNumber10 = checkFloat(data['progress'][17])
			event.metricNumber11 = checkFloat(data['progress'][18])
			event.metricNumber12 = checkFloat(data['progress'][19])
			event.metricNumber13 = checkFloat(data['progress'][20])
			event.metricNumber14 = checkFloat(data['progress'][21])
			event.metricNumber15 = checkFloat(data['progress'][22])
			event.metricNumber16 = checkFloat(data['progress'][23])
			event.metricNumber17 = checkFloat(data['progress'][24])
			event.metricNumber18 = checkFloat(data['progress'][25])
			event.metricNumber19 = checkFloat(data['progress'][26])
			event.metricNumber20 = checkFloat(data['progress'][27])
			event.metricNumber21 = checkFloat(data['progress'][28])
			event.metricNumber22 = checkFloat(data['progress'][29])
			event.metricNumber23 = checkFloat(data['progress'][30])
			event.metricNumber24 = checkFloat(data['progress'][31])
		except Exception:
			raise EventProgressMetricFormatError()

		# If attributes defined, add them to the event
		if 'attributes' in data:
			if len(data['attributes']) != 16:
				raise EventMissingAttributeError()

			try:
				event.attributeString1 = checkString(data['attributes'][0])
				event.attributeString2 = checkString(data['attributes'][1])
				event.attributeString3 = checkString(data['attributes'][2])
				event.attributeString4 = checkString(data['attributes'][3])
				event.attributeNumber1 = checkFloat(data['attributes'][4])
				event.attributeNumber2 = checkFloat(data['attributes'][5])
				event.attributeNumber3 = checkFloat(data['attributes'][6])
				event.attributeNumber4 = checkFloat(data['attributes'][7])
				event.attributeNumber5 = checkFloat(data['attributes'][8])
				event.attributeNumber6 = checkFloat(data['attributes'][9])
				event.attributeNumber7 = checkFloat(data['attributes'][10])
				event.attributeNumber8 = checkFloat(data['attributes'][11])
				event.attributeNumber9 = checkFloat(data['attributes'][12])
				event.attributeNumber10 = checkFloat(data['attributes'][13])
				event.attributeNumber11 = checkFloat(data['attributes'][14])
				event.attributeNumber12 = checkFloat(data['attributes'][15])
			except Exception:
				raise EventAttributeFormatError()

		return event



	def processUpdates(self):
		
		totalFiles = self.storage.count()

		for i, filename in enumerate(self.storage.getFiles()):
			if 'json' in filename:
				print('[%d of %d] Processing...'%(i, totalFiles))
				self.processUpdate(filename)


		

	def exportData(self, fromDate, toDate):
		pass

