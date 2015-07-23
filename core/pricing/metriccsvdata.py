import csv
import io

from core.pricing.engine import DataEngine
from core.pricing.exceptions import *


class MetricCSVDataEngine(DataEngine):
	def getPrices(self, progress, country=None):
		if type(self.data['metric']) == int:
			p = progress[self.data['metric']]
		elif self.data['metric'] == 'country':
			p = country
		
		if type(p) == str:
			p = p.strip().lower()

		if p in self.data['data']:
			return self.data['data'][p]

		return self.data['data']['default']

	@staticmethod
	def validate(prices):
		raw = DataEngine.getData(prices).strip()

		raw = csv.reader(io.StringIO(raw))
		rows = list(raw)

		if len(rows) < 2:
			raise DataEngineException('Must contain at least two rows')
		if len(rows[0]) < 2:
			raise DataEngineException('Must contain at least two columns')

		try:
			metric = rows[0][0]
			if 'metricString' in metric:
				metric = int(metric[12:])-1
			elif 'metricNumber' in metric:
				metric = int(metric[12:])+8-1
			elif metric.lower().strip() == 'country':
				metric = metric.lower().strip()
			else:
				assert(False)
			assert((type(metric)==int and metric<32 and metric>-1) or (metric=='country'))
		except:
			raise DataEngineException('Metric name not valid/recognized')

		if type(metric) == int:
			if metric<8:
				progress = list(map(lambda p: p.strip().lower(), rows[0][1:]))
			else:
				try:
					progress = []
					for p in rows[0][1:]:
						if p.strip().lower() == 'default':
							progress.append('default')
						else:
							progress.append(float(p))
				except: 
					raise DataEngineException('Numberic progress metric must have numeric progress values for the columns')
		elif type(metric) == str:
			progress = list(map(lambda p: p.strip().lower(), rows[0][1:]))

		data = dict(map(lambda p: (p, {}), progress))

		if any(map(lambda p: p.lower() == 'default', progress)) == False:
			raise DataEngineException('Missing default pricing column')
		
		for row in rows[1:]:
			# Remove trailing spaces
			row = list(map(lambda r: r.strip(), row))

			if len(row) != len(row[0]):
				raise DataEngineException('All rows must contain the same number of elements')
			
			for i, value in enumerate(row[1:]):
				try:
					data[progress[i]][row[0]] = [float(value)] + [None]*7
				except:
					raise DataEngineException('The first column must be a tring, all other columns must be good prices encoded as numbers')

		return {'metric':metric, 'data':data}

