from multiprocessing import Pool
import time
import numpy

import core.util.rest
import core.content.content as content
from core.util.test import *
import core.util.extras as extras
import core.api.main as main
import config
from core.util.test import *


def makeRequest(*args, **kwargs):
	global api, application

	data = {
		'user': '0'*32,
		'events': [
			{
				'name': 'liftpass-metric',
				'progress': ['','','','','','','','']+[0]*24,
				'time': extras.unixTimestamp()
			}
		]
	}

	start = time.time()
	(status, b) = api.request('POST', '/sdk/update/v1/', data, application=application)
	data['user'] = '1'*32
	(status, c) = api.request('POST', '/sdk/update/v1/', data, application=application)
	
	return time.time() - start


class StressTest(APITest):
	def testBlank(self):
		pass

api = discoverTests(StressTest, config.APIServer['address'], config.APIServer['port'], config.UserKey, config.UserSecret, main.app)[0]
backend = content.Content()
application = backend.addApplication('Test SDK')

jsonPricesA = backend.addPrices(application.key, 'JSON', json.dumps({'sword':1000}), None)
jsonPricesB = backend.addPrices(application.key, 'JSON', json.dumps({'sword':2000}), None)

backend.setABTest(application.key, {'groupAPrices_key': jsonPricesA.key})
backend.setABTest(application.key, {'groupBPrices_key': jsonPricesB.key})

def runSingleThread():
	for i in range(1000):
		makeRequest()

def run():
	
	simultaneous = [10, 100, 200, 300, 400, 500]

	for simul in simultaneous:
		with Pool(simul) as p:
			res = p.map(makeRequest, range(10*simul))
			print('%d: %.05f %.05f %.05f'%(simul, numpy.sum(res), numpy.mean(res), numpy.std(res)))

def analyze():
	import cProfile
	cProfile.runctx('runSingleThread()', globals(), locals())