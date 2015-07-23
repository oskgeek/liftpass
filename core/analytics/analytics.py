import json
import datetime
import time
import multiprocessing
import functools
from geolite2 import geolite2

import core.storage as storage
import core.util.extras as extras
import core.util.debug as debug
import core.content.models as models
from core.content.content import Content
import core.monitoring as monitor


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
		self.cachedApplications = {}

	def saveUpdate(self, update):
		monitor.getMonitor().count('AnalyticsSaveUpdateCount')

		key = '%s-%s-%s.json'%(update['liftpass-application'], extras.datetimeStamp(), update['user'])
		self.storage.save(key, json.dumps(update))



	def processUpdate(self, data, session=None):
		monitor.getMonitor().count('AnalyticsProcessUpdateCount')

		with monitor.getMonitor().time('AnalyticsProcessUpdateTime'):
			for attribute in ['liftpass-ip', 'liftpass-application', 'user', 'events']:
				if attribute not in data:
					monitor.getMonitor().count('AnalyticsUpdateMissingAttributeCount')
					raise EventMissingAttributeError(attribute)
			
			events = []
			ip = data['liftpass-ip']
			
			try:
				country = geolite2.reader().get(ip)
				country = country['country']['iso_code']
			except:
				country = None

			s = time.time()
			for update in data['events']:
				try:
					with monitor.getMonitor().time('AnalyticsProcessUpdateEventTime'):
						monitor.getMonitor().count('AnalyticsEventCount')
						events.append(self.processEvent(data['liftpass-application'], data['user'], ip, country, update))
				except Exception as e:
					print(e)

		if session != None: 
			session.execute(models.Events.__table__.insert(), events)
			session.commit()

		return events



	def processEvent(self, application, user, ip, country, data):
		if 'name' not in data:
			monitor.getMonitor().count('AnalyticsEventMissingNameCount')
			raise EventAttributeMissingError('name')
		if 'time' not in data:
			monitor.getMonitor().count('AnalyticsEventMissingTimeCount')
			raise EventAttributeMissingError('time')
		if 'progress' not in data:
			monitor.getMonitor().count('AnalyticsEventMissingProgressCount')
			raise EventAttributeMissingError('progress')
		if len(data['progress']) != 32:
			monitor.getMonitor().count('AnalyticsEventIncompleteProgressCount')
			raise EventMissingMetricError()

		event = {}
		event['application_key'] = application
		event['user'] = user
		event['name'] = data['name']
		event['ip'] = ip
		event['country'] = country


		try:
			event['timestamp'] = datetime.datetime.utcfromtimestamp(data['time'])
		except:
			monitor.getMonitor().count('AnalyticsEventBadTimeCount')
			raise EventTimestampError()

		# Try processing each progress metric
		try:
			event['metricString1'] = checkString(data['progress'][0])
			event['metricString2'] = checkString(data['progress'][1])
			event['metricString3'] = checkString(data['progress'][2])
			event['metricString4'] = checkString(data['progress'][3])
			event['metricString5'] = checkString(data['progress'][4])
			event['metricString6'] = checkString(data['progress'][5])
			event['metricString7'] = checkString(data['progress'][6])
			event['metricString8'] = checkString(data['progress'][7])
			event['metricNumber1'] = checkFloat(data['progress'][8])
			event['metricNumber2'] = checkFloat(data['progress'][9])
			event['metricNumber3'] = checkFloat(data['progress'][10])
			event['metricNumber4'] = checkFloat(data['progress'][11])
			event['metricNumber5'] = checkFloat(data['progress'][12])
			event['metricNumber6'] = checkFloat(data['progress'][13])
			event['metricNumber7'] = checkFloat(data['progress'][14])
			event['metricNumber8'] = checkFloat(data['progress'][15])
			event['metricNumber9'] = checkFloat(data['progress'][16])
			event['metricNumber10'] = checkFloat(data['progress'][17])
			event['metricNumber11'] = checkFloat(data['progress'][18])
			event['metricNumber12'] = checkFloat(data['progress'][19])
			event['metricNumber13'] = checkFloat(data['progress'][20])
			event['metricNumber14'] = checkFloat(data['progress'][21])
			event['metricNumber15'] = checkFloat(data['progress'][22])
			event['metricNumber16'] = checkFloat(data['progress'][23])
			event['metricNumber17'] = checkFloat(data['progress'][24])
			event['metricNumber18'] = checkFloat(data['progress'][25])
			event['metricNumber19'] = checkFloat(data['progress'][26])
			event['metricNumber20'] = checkFloat(data['progress'][27])
			event['metricNumber21'] = checkFloat(data['progress'][28])
			event['metricNumber22'] = checkFloat(data['progress'][29])
			event['metricNumber23'] = checkFloat(data['progress'][30])
			event['metricNumber24'] = checkFloat(data['progress'][31])
		except Exception:
			monitor.getMonitor().count('AnalyticsEventBadMetricCount')
			raise EventProgressMetricFormatError()

		# If attributes defined, add them to the event
		if 'attributes' in data:
			if len(data['attributes']) != 16:
				raise EventMissingAttributeError()

			try:
				event['attributeString1'] = checkString(data['attributes'][0])
				event['attributeString2'] = checkString(data['attributes'][1])
				event['attributeString3'] = checkString(data['attributes'][2])
				event['attributeString4'] = checkString(data['attributes'][3])
				event['attributeNumber1'] = checkFloat(data['attributes'][4])
				event['attributeNumber2'] = checkFloat(data['attributes'][5])
				event['attributeNumber3'] = checkFloat(data['attributes'][6])
				event['attributeNumber4'] = checkFloat(data['attributes'][7])
				event['attributeNumber5'] = checkFloat(data['attributes'][8])
				event['attributeNumber6'] = checkFloat(data['attributes'][9])
				event['attributeNumber7'] = checkFloat(data['attributes'][10])
				event['attributeNumber8'] = checkFloat(data['attributes'][11])
				event['attributeNumber9'] = checkFloat(data['attributes'][12])
				event['attributeNumber10'] = checkFloat(data['attributes'][13])
				event['attributeNumber11'] = checkFloat(data['attributes'][14])
				event['attributeNumber12'] = checkFloat(data['attributes'][15])
			except Exception:
				monitor.getMonitor().count('AnalyticsEventBadAttributeCount')
				raise EventAttributeFormatError()

		return event

	def getApplication(self, application):
		if application not in self.cachedApplications:
			content = Content()
			self.cachedApplications[application] = (content.getApplicationExists(application) > 0)
		return self.cachedApplications[application]


	def processThreadUpdate(self, filenames):
		session = models.getSession()		

		eventsCount = 0
		events = []

		for filename in filenames:
			if 'json' in filename:
				
				try:
					data = self.storage.load(filename)
					data = json.loads(data)
				except:
					self.storage.delete(filename)
					continue

				if self.getApplication(data['liftpass-application']) != None:
					currentEvents = self.processUpdate(data)
					eventsCount += len(currentEvents)
					events.extend(currentEvents)

				self.storage.delete(filename)

			if len(events) > 1000:
				session.execute(models.Events.__table__.insert(), events)
				events = []

		session.execute(models.Events.__table__.insert(), events)
		session.commit()

		return eventsCount

	def processUpdates(self, processors = 1, limit = 100):
		content = Content()

		updates = self.storage.getFiles()

		start = time.time()
		count = 0
		events = 0
		

		queue = []
		for p in range(processors):
			queue.append(list(map(lambda x: updates.__next__(), range(limit))))

		if processors == 1:
			for q in queue:
				events += self.processThreadUpdate(q)
		else:
			pool = multiprocessing.Pool(processors)
			events = pool.map(self.processThreadUpdate, queue)
			events = sum(events)
		

		count = len(queue)
		elapse = time.time()-start

		print('-'*30)
		print('Analyzed %d and %d events.\n1 update per %.03fsec\n1 event per %.03fsec'%(count, events, elapse*1.0/count, elapse*1.0/events))
		

	def exportStream(self, application, fromDate, toDate, streaming = True):
		session = models.getSession()
		
		q = session.query(models.Events).filter_by(application_key=application).all()#, models.Events.created>=fromDate, models.Events.created<toDate)
		out = ''

		for row in q:

			if streaming:
				yield extras.toJSON(row.as_dict())+'\n'
			else:
				out += extras.toJSON(row.as_dict())+'\n'
		
		if streaming == False:
			return out


