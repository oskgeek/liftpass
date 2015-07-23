import statsd
import threading
import time

connection = None
connectionLock = threading.Lock()

class StatsDTimer:

	def __init__(self, monitor, metric):
		self.monitor = monitor
		self.metric = metric

		
	def __enter__(self):
		self.start = time.time()

	def __exit__(self, type, value, traceback):
		self.monitor.put(self.metric, (time.time()-self.start)*1000, 'Milliseconds')


class StatsD:

	def __init__(self, settings):
		with connectionLock:
			global connection
			if connection == None:
				connection = statsd.Connection(host=settings['host'], port=settings['port'], sample_rate=1, disabled=False)
		self.namespace = settings['namespace']
	

	def put(self, metric, value, units):
		with connectionLock:
			global connection
			statsd.Counter(self.namespace, connection).increment(metric, value)

	def count(self, metric):
		with connectionLock:
			global connection
			statsd.Counter(self.namespace, connection).increment(metric, 1)

	def time(self, metric):
		return StatsDTimer(self, metric)
