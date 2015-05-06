import json

import config
import core.util.debug as debug


class DataEngine:
	def getPrices(self, progress):
		debug.error('DataEngine function not implemented')

class JSONDataEngine(DataEngine):

	def __init__(self, prices):
		if prices['data'] != None:
			self.data = json.loads(prices['data'])
		else:
			debug.error('JSON data engine does not support path field')
			self.data = {}

	def getPrices(self, progress):
		res = {}
		for g in self.data:
			if isinstance(self.data[g], list):
				res[g] = self.data[g]
			else:
				res[g] = [self.data[g]]+[None]*7
		return res


class ApplicationNotFoundException(Exception):
	def __str__(self):
		return 'No application found given the application key'

class NoPricingForGroup(Exception):
	def __str__(self):
		return 'Application has no defined prices for group'


class PricingEngine:


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


	def getPrices(self, user, progress):
		
		userID = int(user, 16)
		
		if userID % self.abtest['modulus'] <= self.abtest['modulusLimit']:
			if self.groupAPrices:
				return self.groupAPrices.getPrices(progress)
			else:
				raise NoPricingForGroup()
		else:
			if self.groupBPrices:
				return self.groupBPrices.getPrices(progress)
			else:
				raise NoPricingForGroup()

		return None

	def __loadPrices(self, prices_key):
		import core.content.content as content
		backend = content.Content()

		data = backend.getPrice(prices_key).as_dict()

		if data['engine'] == 'JSON':
			return JSONDataEngine(data)

		return None