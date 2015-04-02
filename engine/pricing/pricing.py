import json

import config
from core import factory
from util import debug



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


class GameNotFoundException(Exception):
	pass
class NoPricingForGroup(Exception):
	pass
class GameHasNoPrices(Exception):
	pass

class PricingEngine:


	def __init__(self, game_key):
		content = factory.getContent()

		self.dynamicPrices = None
		self.staticPrices = None

		self.abtest = content.getABTest(game_key)
		
		# If there is no AB test for game.. we are done
		if self.abtest == None:
			raise GameNotFoundException()
		
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
		content = factory.getContent()

		data = content.getPrice(prices_key).as_dict()

		if data['engine'] == 'JSON':
			return JSONDataEngine(data)

		return None