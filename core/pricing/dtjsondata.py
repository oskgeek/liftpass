import json

import core.util.debug as debug
from core.pricing.engine import DataEngine
from core.pricing.exceptions import *

class DTJSONData(DataEngine):

	def getPrices(self, progress):
		root = self.data

		while True:
			if all(map(lambda k: k in root, ['metric', 'method', 'keys', 'values'])):
				index = root['metric']

				if root['method'] == 'lookup':
					for i, key in enumerate(root['keys']):
						if progress[index] in set(key):
							root = root['values'][i]
							continue


				elif root['method'] == 'range':
					for i, key in enumerate(root['keys']):
						if progress[index] >= key[0] and progress[index] <= key[1]:
							root = root['values'][i]
							continue

				else:
					return {}
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

