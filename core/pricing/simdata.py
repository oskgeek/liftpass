import json

from core.pricing.engine import DataEngine
from core.pricing.exceptions import *

class SimDataEngine(DataEngine):

	def getPrices(self, progress, country=None):
		res = {}
		for g in self.data['prices']:
			if isinstance(self.data['prices'][g], list):
				res[g] = self.data['prices'][g]
			else:
				res[g] = [self.data['prices'][g]]+[None]*7

		for g in res:
			try:
				res[g][0] += progress[self.data['metric']]
			except:
				pass

		return res

	@staticmethod
	def validate(prices):
		raw = DataEngine.getData(prices).strip()

		try:
			data = json.loads(raw)
		except:
			raise DataEngineException('JSON data failed to be parsed')

		if 'prices' not in data:
			raise DataEngineException('Sim data must have prices key')
		if 'metric' not in data:
			raise DataEngineException('Sim data must have metric key')

		if type(data['metric']) != int:
			raise DataEngineException('Metric must be an integer between 0 and 31')

		for k in data['prices']:
			if type(k) != str:
				raise DataEngineException('Keys must be strings')
			if type(data['prices'][k]) not in (int, list, float):
				raise DataEngineException('Values must be arrays or numbers')
			if type(data['prices'][k]) == list:
				if len(data['prices'][k]) != 8:
					raise DataEngineException('Array values must have exactly 8 elements')
				if any(map(lambda i: type(i) not in [int, float, type(None)], data['prices'][k])):
					raise DataEngineException('Array values must be all numbers or null')
		return data

