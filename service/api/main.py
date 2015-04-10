import hmac
import hashlib
import json
from flask import Flask
from flask import request


import service.service as service
import config

from core import factory
import service.api.errors as errors
import util.rest as rest
import util.debug as debug

app = Flask(__name__)

def userAuthenticate(f):
	def aux(*args, **kwargs):
		# JSON must include time and user key
		if not all(map(lambda k: k in request.json, ['gondola-time', 'gondola-user'])):
			return rest.errorResponse(errors.RequestMissingArguments)

		# HTTP header must include hash for all requests
		if 'gondola-hash' not in request.headers:
			return rest.errorResponse(errors.RequestMissingArguments)

		digest = hmac.new(config.UserSecret, request.get_data(), hashlib.sha256).hexdigest()

		if digest != request.headers['gondola-hash']:
			return rest.errorResponse(errors.FailedToAuthenticate)
		
		return f(*args, **kwargs)
	return aux

@app.route('/games/add/<version>/', methods=['POST'])
@userAuthenticate
def gameAdd(version):
	"""
	Adds new game to the system. 

	Arguments:
	name -- the key for the game
	"""
	content = factory.getContent()	

	game = content.addGame(request.json['name'])
	
	return rest.successResponse(game.as_dict())

@app.route('/games/list/<version>/', methods=['GET'])
def gameList(version):
	"""
	Gets list of games.
	"""
	content = factory.getContent()
	games = content.getGames()
	
	result = list(map(lambda g: g.as_dict(), games))
	
	return rest.successResponse({'games': result})

@app.route('/games/delete/<version>/', methods=['DELETE'])
def gameDelete(version):
	"""
	Deletes game and supporting data.

	Arguments:
	key -- the key for the game
	"""
	content = factory.getContent()
	success = content.deleteGame(request.json['key'])
	
	if success:
		return rest.successResponse({'deleted': success>0})
	return rest.errorResponse(errors.GameKeyDoesNotExist)

@app.route('/games/get/<version>/', methods=['GET'])
def gameGet(version):
	"""
	Gets information about game.

	Arguments:
	key -- the key for the game
	"""
	content = factory.getContent()	
	game = content.getGame(request.json['key'])
	if game:
		return rest.successResponse(game.as_dict())
	
	return rest.errorResponse(errors.GameKeyDoesNotExist)

@app.route('/games/update/<version>/', methods=['PUT'])
def gameUpdate(version):
	"""
	Updates game information.

	Arguments:
	key -- the game key
	name -- (optional) the name of the game 

	"""
	content = factory.getContent()

	game = content.setGame(request.json['key'], request.json)

	if game:
		return rest.successResponse(game.as_dict())
	return rest.errorResponse(errors.GameKeyDoesNotExist)

@app.route('/currencies/get/<version>/', methods=['GET'])
def currencyGet(version):
	"""
	Get currency for the specified game.

	Arguments:
	key -- the game key
	"""
	content = factory.getContent()

	currency = content.getCurrency(request.json['key'])
	if currency:
		return rest.successResponse(currency.as_dict())
	return rest.errorResponse(errors.GameKeyDoesNotExist)

@app.route('/currencies/update/<version>/', methods=['PUT'])
def currencyUpdate(version):
	"""
	Updates a single currency name for the game specified.

	Arguments:
	key -- the game key
	name1 to name8 -- name of currencies in the game
	"""

	content = factory.getContent()

	currency = content.setCurrency(request.json['key'], request.json)
	if currency:
		return rest.successResponse(currency.as_dict())
	return rest.errorResponse(errors.GameKeyDoesNotExist)

@app.route('/goods/add/<version>/', methods=['POST'])
def goodsAdd(version):
	content = factory.getContent()
	good = content.addGood(request.json['key'], request.json['name'])
	return rest.successResponse(good.as_dict())

@app.route('/goods/get/<version>/', methods=['GET'])
def goodsGet(version):
	content = factory.getContent()
	good = content.getGood(request.json['key'])
	if good:
		return rest.successResponse(good.as_dict())
	return rest.errorResponse(errors.GoodKeyDoesNotExist)

@app.route('/goods/list/<version>/', methods=['GET'])
def goodsList(version):
	content = factory.getContent()
	goods = content.getGoods(request.json['key'])
	results = list(map(lambda g: g.as_dict(), goods))
	return rest.successResponse({'goods': results})

@app.route('/goods/delete/<version>/', methods=['DELETE'])
def goodsDelete(version):
	content = factory.getContent()
	res = content.deleteGood(request.json['key'])
	return rest.successResponse({'deleted':res>0})

@app.route('/goods/update/<version>/', methods=['PUT'])
def goodsUpdate(version):
	content = factory.getContent()
	good = content.updateGood(request.json['key'], request.json)
	if good:
		return rest.successResponse(good.as_dict())
	return rest.errorResponse(errors.GoodKeyDoesNotExist)

@app.route('/abtest/get/<version>/', methods=['GET'])
def abtestGet(version):
	content = factory.getContent()
	abtest = content.getABTest(request.json['key'])
	if abtest:
		return rest.successResponse(abtest.as_dict())
	return rest.errorResponse(errors.GameKeyDoesNotExist)

@app.route('/abtest/update/<version>/', methods=['PUT'])
def abtestUpdate(version):
	content = factory.getContent()
	abtest = content.setABTest(request.json['key'], request.json)
	return rest.successResponse(abtest.as_dict())

@app.route('/metrics/get/<version>/', methods=['GET'])
def metricsGet(version):
	content = factory.getContent()
	metrics = content.getMetrics(request.json['key'])
	if metrics:
		return rest.successResponse(metrics.as_dict())
	return rest.errorResponse(errors.GameKeyDoesNotExist)

@app.route('/metrics/update/<version>/', methods=['PUT'])
def metricsUpdate(version):
	content = factory.getContent()
	metrics = content.setMetrics(request.json['key'], request.json)
	return rest.successResponse(metrics.as_dict())

@app.route('/prices/list/<version>/', methods=['GET'])
def pricesList(version):
	content = factory.getContent()
	prices = content.getPrices(request.json['key'])
	prices = list(map(lambda p: p.as_dict(), prices))
	return rest.successResponse({'prices':prices})

@app.route('/prices/get/<version>/', methods=['GET'])
def pricesGet(version):
	content = factory.getContent()
	prices = content.getPrice(request.json['key'])
	if prices:
		return rest.successResponse(prices.as_dict())
	return rest.errorResponse(errors.PricesKeyDoesNotExist)

@app.route('/prices/delete/<version>/', methods=['DELETE'])
def pricesDelete(version):
	content = factory.getContent()
	res = content.deletePrices(request.json['key'])
	return rest.successResponse({'deleted': res>0})

@app.route('/prices/add/<version>/', methods=['POST'])
def pricesAdd(version):
	content = factory.getContent()
	prices = content.addPrices(request.json['key'], request.json['engine'], request.json['data'], request.json['path'])
	return rest.successResponse(prices.as_dict())

@app.errorhandler(500)
def page_not_found(e):
	debug.error('%s'%e)
	return rest.errorResponse({'status': 500, 'message':str(e)})

def start():
	global app
	app.run(debug=config.APIDebug, port=config.APIPort)

def getApp():
	global app
	return app