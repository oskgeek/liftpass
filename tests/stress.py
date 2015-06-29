from multiprocessing import Pool
import time
import numpy
import random

import core.util.rest
import core.content.content as content
from core.util.test import *
import core.util.extras as extras
import core.api.main as main
import config
from core.util.test import *

def makeProgress(length):

	progress = ['','','','','','','','']+[0]*24
	res = []
	for i in range(length):
		progress[random.randint(8, 31)] += 1
		
		res.append({
				'name': 'liftpass-metric',
				'progress': progress[:],
				'time': extras.unixTimestamp()+i
		})
	return res

def makeRequest(*args, **kwargs):
	global api, application

	data = {
		'user': '0'*32,
		'events': makeProgress(25)
	}

	start = time.time()
	
	try:
		(status, b) = api.request('POST', '/sdk/update/v1/', data, application=application, forceNetwork=True)
		# data['user'] = '1'*32
		# (status, c) = api.request('POST', '/sdk/update/v1/', data, application=application, forceNetwork=True)
	except: 
		return None

	if status != 200:
		return None
	
	return time.time() - start


class StressTest(APITest):
	def testBlank(self):
		pass

# api = discoverTests(StressTest, config.APIServer['address'], config.APIServer['port'], config.UserKey, config.UserSecret, main.app)[0]
api = discoverTests(StressTest, '54.175.122.247', 80, config.UserKey, config.UserSecret, main.app)[0]
backend = content.Content()

application = backend.getApplicationWithName('Test SDK') 
if application == None:
	application = backend.addApplication('Test SDK')

jsonPricesA = backend.addPrices(application.key, 'JSON', json.dumps({'sword':1000}), None)
jsonPricesB = backend.addPrices(application.key, 'JSON', json.dumps({'sword':2000}), None)

backend.setABTest(application.key, {'groupAPrices_key': jsonPricesA.key})
backend.setABTest(application.key, {'groupBPrices_key': jsonPricesB.key})

def runSingleThread():
	iterations = 1000
	res = list(map(lambda i: makeRequest(), range(iterations)))

	print('%d: %.05f %.05f %.05f'%(iterations, numpy.sum(res), numpy.mean(res), numpy.std(res)))

def run():
	
	# runSingleThread()	
	simultaneous = [4]#, 100, 200, 300, 400, 500]
	iterations = 10
	for simul in simultaneous:
		p = Pool(simul)
		res = p.map(makeRequest, range(iterations))

		good = list(filter(lambda x: x != None, res))


		print('Iterations%d'%simul)
		print('Success Rate:%d/%d Total Time:%.05f Mean:%.05f Std:%.05f'%(len(good), simul, numpy.sum(good), numpy.mean(good), numpy.std(good)))

# def analyze():
# 	import cProfile
# 	cProfile.runctx('runSingleThread()', globals(), locals())