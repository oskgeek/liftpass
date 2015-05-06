import hmac
import hashlib
import json
from functools import wraps
from functools import update_wrapper

from flask import Flask
from flask import request
from flask import make_response
from flask.ext.cors import CORS

import config
import core.content.content as content
import core.storage as storage
import core.pricing.pricing as pricing
import core.analytics.analytics as analytics

import core.content.errors as errors
import core.util.rest as rest
import core.util.debug as debug
import core.util.extras as extras
import core.dashboard.terminal as terminal


app = Flask(__name__)
CORS(app)


@app.route('/applications/add/<version>/', methods=['POST'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def applicationAdd(version):
	"""
	Adds new application to the system. 

	Arguments:
	name -- the key for the application
	"""

	backend = content.Content()

	application = backend.addApplication(request.values['name'])
	
	return application.as_dict()


@app.route('/applications/list/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def applicationList(version):
	"""
	Gets list of applications.
	"""
	backend = content.Content()
	applications = backend.getApplications()
	
	result = list(map(lambda g: g.as_dict(), applications))
	
	return {'applications': result}


@app.route('/applications/delete/<version>/', methods=['DELETE'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def applicationDelete(version):
	"""
	Deletes application and supporting data.

	Arguments:
	key -- the key for the application
	"""
	backend = content.Content()
	success = backend.deleteApplication(request.values['key'])
	
	if success:
		return {'deleted': success>0}
	return errors.ApplicationKeyDoesNotExist


@app.route('/applications/get/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def applicationGet(version):
	"""
	Gets information about application.

	Arguments:
	key -- the key for the application
	"""
	backend = content.Content()	
	application = backend.getApplication(request.values['key'])
	if application:
		return application.as_dict()
	
	return errors.ApplicationKeyDoesNotExist


@app.route('/applications/update/<version>/', methods=['PUT'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def applicationUpdate(version):
	"""
	Updates application information.

	Arguments:
	key -- the application key
	name -- (optional) the name of the application 

	"""
	backend = content.Content()

	application = backend.setApplication(request.values['key'], request.values)

	if application:
		return application.as_dict()
	return errors.ApplicationKeyDoesNotExist


@app.route('/currencies/get/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def currencyGet(version):
	"""
	Get currency for the specified application.

	Arguments:
	key -- the application key
	"""
	backend = content.Content()

	currency = backend.getCurrency(request.values['key'])
	if currency:
		return currency.as_dict()
	return errors.ApplicationKeyDoesNotExist


@app.route('/currencies/update/<version>/', methods=['PUT'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def currencyUpdate(version):
	"""
	Updates a single currency name for the application specified.

	Arguments:
	key -- the application key
	currency1 to currency8 -- name of currencies in the application
	"""

	backend = content.Content()

	currency = backend.setCurrency(request.values['key'], request.values)
	if currency:
		return currency.as_dict()
	return errors.ApplicationKeyDoesNotExist


@app.route('/goods/add/<version>/', methods=['POST'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def goodsAdd(version):
	backend = content.Content()
	good = backend.addGood(request.values['key'], request.values['name'])
	return good.as_dict()


@app.route('/goods/get/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def goodsGet(version):
	backend = content.Content()
	good = backend.getGood(request.values['key'])
	if good:
		return good.as_dict()
	return errors.GoodKeyDoesNotExist


@app.route('/goods/list/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def goodsList(version):
	backend = content.Content()
	goods = backend.getGoods(request.values['key'])
	results = list(map(lambda g: g.as_dict(), goods))
	return {'goods': results}


@app.route('/goods/delete/<version>/', methods=['DELETE'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def goodsDelete(version):
	backend = content.Content()
	res = backend.deleteGood(request.values['key'])
	return {'deleted':res>0}


@app.route('/goods/update/<version>/', methods=['PUT'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def goodsUpdate(version):
	backend = content.Content()
	good = backend.updateGood(request.values['key'], request.values)
	if good:
		return good.as_dict()
	return errors.GoodKeyDoesNotExist


@app.route('/abtest/get/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def abtestGet(version):
	backend = content.Content()
	abtest = backend.getABTest(request.values['key'])
	if abtest:
		return abtest.as_dict()
	return errors.ApplicationKeyDoesNotExist


@app.route('/abtest/update/<version>/', methods=['PUT'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def abtestUpdate(version):
	backend = content.Content()
	abtest = backend.setABTest(request.values['key'], request.values)
	return abtest.as_dict()


@app.route('/metrics/get/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def metricsGet(version):
	backend = content.Content()
	metrics = backend.getMetrics(request.values['key'])
	if metrics:
		return metrics.as_dict()
	return errors.ApplicationKeyDoesNotExist


@app.route('/metrics/update/<version>/', methods=['PUT'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def metricsUpdate(version):
	backend = content.Content()
	metrics = backend.setMetrics(request.values['key'], request.values)
	return metrics.as_dict()


@app.route('/prices/list/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def pricesList(version):
	backend = content.Content()
	prices = backend.getPrices(request.values['key'])
	prices = list(map(lambda p: p.as_dict(), prices))
	return {'prices':prices}


@app.route('/prices/get/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def pricesGet(version):
	backend = content.Content()
	prices = backend.getPrice(request.values['key'])
	if prices:
		return prices.as_dict()
	return errors.PricesKeyDoesNotExist


@app.route('/prices/delete/<version>/', methods=['DELETE'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def pricesDelete(version):
	backend = content.Content()
	res = backend.deletePrices(request.values['key'])
	return {'deleted': res > 0}


@app.route('/prices/add/<version>/', methods=['POST'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def pricesAdd(version):
	backend = content.Content()
	prices = backend.addPrices(request.values['key'], request.values['engine'], request.values['data'], request.values['path'])
	return prices.as_dict()


def terminalLog():
	def decorator(f): 
		def aux(*args, **kwargs):
			response = f(*args, **kwargs)
			
			if 'liftpass-application' in request.values and 'liftpass-debug' in request.values:
				if request.values['liftpass-debug'] == True:
					theTerminal = terminal.getTerminal()
					theTerminal.put(request.values['liftpass-application'], request.values, json.loads(response.data.decode('utf-8')))

			return response
		return update_wrapper(aux, f)
	return decorator




@app.route('/sdk/update/<version>/', methods=['POST'])
@terminalLog()
@rest.applicationAuthenticate(secretLookup=content.Content().getApplicationSecret)
def update(version):
	theTerminal = terminal.getTerminal()

	backend = content.Content()
	theAnalytics = analytics.Analytics()

	# Check minimum number of keys required in JSON update
	if extras.keysInDict(request.values, ['user', 'events']) == False:
		return errors.ApplicationUpdateIncomplete

	# Events must have at least one item
	if len(request.values['events']) == 0:
		return errors.ApplicationUpdateMissingEvents
	
	# Event has progress
	if 'progress' not in request.values['events'][-1]:
		return errors.ApplicationUpdateMissingEvents
	
	# Save update (include IP address of user)
	request.values['liftpass-ip'] = request.remote_addr
	theAnalytics.saveUpdate(request.values)
	
	# Try getting price engine
	try:
		prices = backend.getPricingEngine(request.values['liftpass-application'])
	except pricing.ApplicationNotFoundException:
		return errors.ApplicationKeyDoesNotExist

	# Try getting price for user + progress
	try:
		userPrices = prices.getPrices(request.values['user'], request.values['events'][-1]['progress'])
	except pricing.NoPricingForGroup:
		return errors.ApplicationHasNoPriceForUser

	return {'goods':userPrices}


@app.route('/export/json/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def exportJSON(version):

	theAnalytics = analytics.Analytics()

	fromDate = extras.unixTimestampToDatetime(request.values['from'])
	toDate = extras.unixTimestampToDatetime(request.values['to'])

	return rest.streamResponse(lambda: theAnalytics.exportStream(request.values['application'], fromDate, toDate))


@app.errorhandler(500)
def page_not_found(e):
	debug.stacktrace(e)
	return rest.errorResponse({'status': 500, 'message': str(e)})


def start():
	global app
	app.run(debug=config.APIDebug, host=config.APIAddress, port=config.APIPort)


def getApp():
	global app
	return app