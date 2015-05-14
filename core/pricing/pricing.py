import json
import csv
import io

import config
import core.util.debug as debug


from core.pricing.jsondata import *
from core.pricing.csvdata import *
from core.pricing.metriccsvdata import *
from core.pricing.exceptions import *


class PricingEngine:

	cached = {}


	def __init__(self, application_key):
		import core.content.content as content
		backend = content.Content()

		self.groupAPrices = None
		self.groupBPrices = None

		self.abtest = backend.getABTest(application_key)
		
		# If there is no AB test for application.. we are done
		if self.abtest == None:
			raise ApplicationNotFoundException()
		
		self.abtest = self.abtest.as_dict()

		if self.abtest['groupAPrices_key'] != None:
			self.groupAPrices = self.__loadPrices(self.abtest['groupAPrices_key'])
		
		if self.abtest['groupBPrices_key'] != None:
			self.groupBPrices = self.__loadPrices(self.abtest['groupBPrices_key'])

	@staticmethod
	def getApplicationPricing(application_key):
		if application_key not in PricingEngine.cached:
			PricingEngine.cached[application_key] = PricingEngine(application_key)
		return PricingEngine.cached[application_key]


	@staticmethod
	def getPricingEngine(name):
		if name.upper() == 'JSON':
			return JSONDataEngine
		elif name.upper() == 'CSV':
			return CSVDataEngine
		elif name.upper() == 'MetricCSV':
			return MetricCSVDataEngine
		raise DataEngineException('Pricing data engine not recognized')

	
	@staticmethod
	def validate(price):
		if type(price) != dict:
			price = price.as_dict()

		engine = PricingEngine.getPricingEngine(price['engine'])
		if engine == None:
			raise DataEngineException('Unknown pricing engine')

		engine.validate(price)


	def getPrices(self, user, progress):
		
		userID = int(user, 16)
		
		if userID % self.abtest['modulus'] <= self.abtest['modulusLimit']:
			if self.groupAPrices:
				return (self.abtest['groupAPrices_key'], self.groupAPrices.getPrices(progress))
			else:
				raise NoPricingForGroup()
		else:
			if self.groupBPrices:
				return (self.abtest['groupBPrices_key'], self.groupBPrices.getPrices(progress))
			else:
				raise NoPricingForGroup()

		return None


	def __loadPrices(self, prices_key):
		import core.content.content as content
		backend = content.Content()

		data = backend.getPrice(prices_key).as_dict()


		engine = PricingEngine.getPricingEngine(data['engine'])
		if engine == None: 
			raise DataEngineException('Unknown pricing engine')

		return engine(data)
		
