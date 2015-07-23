import json

from core.pricing.engine import DataEngine
from core.pricing.exceptions import *

class JSONDataEngine(DataEngine):

	def getPrices(self, progress, country=None):
		res = {}
		for g in self.data:
			if isinstance(self.data[g], list):
				res[g] = self.data[g]
			else:
				res[g] = [self.data[g]]+[None]*7
		return res

	@staticmethod
	def validate(prices):
		raw = DataEngine.getData(prices).strip()

		try:
			data = json.loads(raw)
		except:
			raise DataEngineException('JSON data failed to be parsed')

		for k in data:
			if type(k) != str:
				raise DataEngineException('Keys must be strings')
			if type(data[k]) not in (int, list, float):
				raise DataEngineException('Values must be arrays or numbers')
			if type(data[k]) == list:
				if len(data[k]) != 8:
					raise DataEngineException('Array values must have exactly 8 elements')
				if any(map(lambda i: type(i) not in [int, float, type(None)], data[k])):
					raise DataEngineException('Array values must be all numbers or null')
		return data

