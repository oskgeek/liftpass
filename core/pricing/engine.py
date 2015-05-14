from core.pricing.exceptions import *
import core.util.debug as debug

import config
import core.storage as storage

class DataEngine:

	def __init__(self, prices):
		try:
			self.data = self.validate(prices)
		except DataEngineException as e:
			debug.error('%s'%e)
			self.data = {}
		except Exception as e:
			self.data = {}

	def getPrices(self, progress):
		debug.error('DataEngine function not implemented')

	@staticmethod
	def validate(prices):
		debug.error('DataEngine function not implemented')


	@staticmethod
	def getData(prices):
		if prices['data'] and len(prices['data'])>1:
			return prices['data']

		store = storage.getStorage(config.PricingStorage)

		return store.load(prices['path'])