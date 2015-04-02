import dbm

import config


class SimpleMonitoring:

	def __init__(self):
		self.db = dbm.open(config.MonitorAddress, 'c')

	def __close__(self):
		self.db.close()
	
	def increment(self, metric, value=1):
		with self.db:
			if self.db[metric]:
				self.db[metric] += value
			else:
				self.db[metric] = value

	def getCount(self, metric):
		with self.db:
			return self.db[metric]


