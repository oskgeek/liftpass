import json

import core.util.debug as debug
from core.pricing.engine import DataEngine
from core.pricing.exceptions import *

class DTJSONData(DataEngine):

	def getPrices(self, progress, country=None):
		root = self.data

		while True:
			if root == None:
				return {}

			if all(map(lambda k: k in root, ['metric', 'method', 'keys', 'values'])):
				index = root['metric']

				defaultIndex = None
				nextRoot = None
				for i, key in enumerate(root['keys']):
					if root['method'] == 'lookup' and progress[index] in set(key):
						nextRoot = root['values'][i]
						break
					elif root['method'] == 'range' and progress[index] >= key[0] and progress[index] <= key[1]:
						nextRoot = root['values'][i]
						break
					elif '*' in key:
						defaultIndex = i

				if nextRoot == None and defaultIndex != None:
					nextRoot = root['values'][defaultIndex]

				root = nextRoot
			else:
				res = {}
				for g in root:
					if isinstance(root[g], list):
						res[g] = root[g]
					else:
						res[g] = [root[g]]+[None]*7
				return res

	@staticmethod
	def validate(prices):
		raw = DataEngine.getData(prices).strip()

		try:
			data = json.loads(raw)
		except:
			raise DataEngineException('JSON data failed to be parsed')

		return data

