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
		return self.data


class ApplicationNotFoundException(Exception):
	pass
class NoPricingForGroup(Exception):
	pass
class ApplicationHasNoPrices(Exception):
	pass

class PricingEngine:


	def __init__(self, application_key):
		import core.content.content as content
		backend = content.Content()

		self.dynamicPrices = None
		self.staticPrices = None

		self.abtest = backend.getABTest(application_key)
		
		# If there is no AB test for application.. we are done
		if self.abtest == None:
			raise ApplicationNotFoundException()
		
		self.abtest = self.abtest.as_dict()

		if self.abtest['dynamicPrices_key'] != None:
			self.dynamicPrices = self.__loadPrices(self.abtest['dynamicPrices_key'])
		
		if self.abtest['staticPrices_key'] != None:
			self.staticPrices = self.__loadPrices(self.abtest['staticPrices_key'])


	def getPrices(self, player, progress):
		
		playerID = int(player, 16)
		
		if playerID % self.abtest['modulus'] <= self.abtest['modulusLimit']:
			if self.dynamicPrices:
				return self.dynamicPrices.getPrices(progress)
			else:
				raise NoPricingForGroup()
		else:
			if self.staticPrices:
				return self.staticPrices.getPrices(progress)
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