import csv
import io

from core.pricing.engine import DataEngine
from core.pricing.exceptions import *


class CSVDataEngine(DataEngine):


	def getPrices(self, progress, country=None):
		return self.data

	@staticmethod
	def validate(prices):
		raw = DataEngine.getData(prices).strip()
		raw = csv.reader(io.StringIO(raw))
		data = {}

		for row in raw:
			if len(row) == 0:
				continue
			elif len(row) > 2 or len(row) == 1:
				raise DataEngineException('Rows must have exactly 2 columns')
			elif len(row) == 2:
				try:
					data[row[0].strip()] = [float(row[1])]+[None]*7
				except:
					raise DataEngineException('The first column must be a string, the second column must be a number')
			elif len(row) == 8:
				try:
					data[row[0].strip()] = []
					for item in row[1:]:
						if item == None: 
							data[row[0].strip()].append(item)
						else:
							data[row[0].strip()].append(float(item))
				except:
					raise DataEngineException('The first column must be a string, the other 8 columns must be numbers')
			else: 
				raise DataEngineException('Prices for goods must either be in a single currency or have 8 currencies defined')
		return data


