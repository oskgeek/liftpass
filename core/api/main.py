import hmac
import hashlib
import json

from flask import Flask
from flask import request

import config
import core.content.content as content
import core.storage as storage
import core.pricing.pricing as pricing
import core.analytics.analytics as analytics

import core.content.errors as errors
import core.util.rest as rest
import core.util.debug as debug
import core.util.extras as extras

app = Flask(__name__)


@app.route('/applications/add/<version>/', methods=['POST'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def applicationAdd(version):
	"""
	Adds new application to the system. 

	Arguments:
	name -- the key for the application
	"""

	backend = content.Content()

	application = backend.addApplication(request.json['name'])
	
	return rest.successResponse(application.as_dict())


@app.route('/applications/list/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def applicationList(version):
	"""
	Gets list of applications.
	"""
	backend = content.Content()
	applications = backend.getApplications()
	
	result = list(map(lambda g: g.as_dict(), applications))
	
	return rest.successResponse({'applications': result})


@app.route('/applications/delete/<version>/', methods=['DELETE'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def applicationDelete(version):
	"""
	Deletes application and supporting data.

	Arguments:
	key -- the key for the application
	"""
	backend = content.Content()
	success = backend.deleteApplication(request.json['key'])
	
	if success:
		return rest.successResponse({'deleted': success>0})
	return rest.errorResponse(errors.ApplicationKeyDoesNotExist)


@app.route('/applications/get/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def applicationGet(version):
	"""
	Gets information about application.

	Arguments:
	key -- the key for the application
	"""
	backend = content.Content()	
	application = backend.getApplication(request.json['key'])
	if application:
		return rest.successResponse(application.as_dict())
	
	return rest.errorResponse(errors.ApplicationKeyDoesNotExist)


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

	application = backend.setApplication(request.json['key'], request.json)

	if application:
		return rest.successResponse(application.as_dict())
	return rest.errorResponse(errors.ApplicationKeyDoesNotExist)


@app.route('/currencies/get/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def currencyGet(version):
	"""
	Get currency for the specified application.

	Arguments:
	key -- the application key
	"""
	backend = content.Content()

	currency = backend.getCurrency(request.json['key'])
	if currency:
		return rest.successResponse(currency.as_dict())
	return rest.errorResponse(errors.ApplicationKeyDoesNotExist)


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

	currency = backend.setCurrency(request.json['key'], request.json)
	if currency:
		return rest.successResponse(currency.as_dict())
	return rest.errorResponse(errors.ApplicationKeyDoesNotExist)


@app.route('/goods/add/<version>/', methods=['POST'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def goodsAdd(version):
	backend = content.Content()
	good = backend.addGood(request.json['key'], request.json['name'])
	return rest.successResponse(good.as_dict())


@app.route('/goods/get/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def goodsGet(version):
	backend = content.Content()
	good = backend.getGood(request.json['key'])
	if good:
		return rest.successResponse(good.as_dict())
	return rest.errorResponse(errors.GoodKeyDoesNotExist)


@app.route('/goods/list/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def goodsList(version):
	backend = content.Content()
	goods = backend.getGoods(request.json['key'])
	results = list(map(lambda g: g.as_dict(), goods))
	return rest.successResponse({'goods': results})


@app.route('/goods/delete/<version>/', methods=['DELETE'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def goodsDelete(version):
	backend = content.Content()
	res = backend.deleteGood(request.json['key'])
	return rest.successResponse({'deleted':res>0})


@app.route('/goods/update/<version>/', methods=['PUT'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def goodsUpdate(version):
	backend = content.Content()
	good = backend.updateGood(request.json['key'], request.json)
	if good:
		return rest.successResponse(good.as_dict())
	return rest.errorResponse(errors.GoodKeyDoesNotExist)


@app.route('/abtest/get/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def abtestGet(version):
	backend = content.Content()
	abtest = backend.getABTest(request.json['key'])
	if abtest:
		return rest.successResponse(abtest.as_dict())
	return rest.errorResponse(errors.ApplicationKeyDoesNotExist)


@app.route('/abtest/update/<version>/', methods=['PUT'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def abtestUpdate(version):
	backend = content.Content()
	abtest = backend.setABTest(request.json['key'], request.json)
	return rest.successResponse(abtest.as_dict())


@app.route('/metrics/get/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def metricsGet(version):
	backend = content.Content()
	metrics = backend.getMetrics(request.json['key'])
	if metrics:
		return rest.successResponse(metrics.as_dict())
	return rest.errorResponse(errors.ApplicationKeyDoesNotExist)


@app.route('/metrics/update/<version>/', methods=['PUT'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def metricsUpdate(version):
	backend = content.Content()
	metrics = backend.setMetrics(request.json['key'], request.json)
	return rest.successResponse(metrics.as_dict())


@app.route('/prices/list/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def pricesList(version):
	backend = content.Content()
	prices = backend.getPrices(request.json['key'])
	prices = list(map(lambda p: p.as_dict(), prices))
	return rest.successResponse({'prices':prices})


@app.route('/prices/get/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def pricesGet(version):
	backend = content.Content()
	prices = backend.getPrice(request.json['key'])
	if prices:
		return rest.successResponse(prices.as_dict())
	return rest.errorResponse(errors.PricesKeyDoesNotExist)


@app.route('/prices/delete/<version>/', methods=['DELETE'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def pricesDelete(version):
	backend = content.Content()
	res = backend.deletePrices(request.json['key'])
	return rest.successResponse({'deleted': res > 0})


@app.route('/prices/add/<version>/', methods=['POST'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def pricesAdd(version):
	backend = content.Content()
	prices = backend.addPrices(request.json['key'], request.json['engine'], request.json['data'], request.json['path'])
	return rest.successResponse(prices.as_dict())


@app.route('/sdk/update/<version>/', methods=['POST'])
@rest.applicationAuthenticate(secretLookup=content.Content().getApplicationSecret)
def update(version):

	backend = content.Content()
	theAnalytics = analytics.Analytics()

	# Check minimum number of keys required in JSON update
	if extras.keysInDict(request.json, ['user', 'events']) == False:
		return rest.errorResponse(errors.ApplicationUpdateIncomplete)

	# Events must have at least one item
	if len(request.json['events']) == 0:
		return rest.errorResponse(errors.ApplicationUpdateMissingEvents)
	
	# Event has progress
	if 'progress' not in request.json['events'][-1]:
		return rest.errorResponse(errors.ApplicationUpdateMissingEvents)
	
	# Save update (include IP address of user)
	request.json['gondola-ip'] = request.remote_addr
	theAnalytics.saveUpdate(request.json)
	
	# Try getting price engine
	try:
		prices = backend.getPricingEngine(request.json['gondola-application'])
	except pricing.ApplicationNotFoundException:
		return rest.errorResponse(errors.ApplicationKeyDoesNotExist)

	# Try getting price for user + progress
	try:
		userPrices = prices.getPrices(request.json['user'], request.json['events'][-1]['progress'])
	except pricing.NoPricingForGroup:
		return rest.errorResponse(errors.ApplicationHasNoPriceForUser)

	return rest.successResponse(userPrices)

@app.route('/export/json/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def exportJSON(version):

	theAnalytics = analytics.Analytics()

	fromDate = extras.unixTimestampToDatetime(request.json['from'])
	toDate = extras.unixTimestampToDatetime(request.json['to'])

	return rest.streamResponse(lambda: theAnalytics.exportStream(request.json['application'], fromDate, toDate))





@app.errorhandler(500)
def page_not_found(e):
	debug.stacktrace(e)
	return rest.errorResponse({'status': 500, 'message': str(e)})


def start():
	global app
	app.run(debug=config.APIDebug, port=config.APIPort)


def getApp():
	global app
	return app