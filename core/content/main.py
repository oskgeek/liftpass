import hmac
import hashlib
import json

from flask import Flask
from flask import request

import config
import core.content.content as content
import core.storage as storage
import core.pricing.pricing as pricing

import core.content.errors as errors
import core.util.rest as rest
import core.util.debug as debug
import core.util.extras as extras

app = Flask(__name__)


@app.route('/games/add/<version>/', methods=['POST'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def gameAdd(version):
	"""
	Adds new game to the system. 

	Arguments:
	name -- the key for the game
	"""

	backend = content.Content()

	game = backend.addGame(request.json['name'])
	
	return rest.successResponse(game.as_dict())


@app.route('/games/list/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def gameList(version):
	"""
	Gets list of games.
	"""
	backend = content.Content()
	games = backend.getGames()
	
	result = list(map(lambda g: g.as_dict(), games))
	
	return rest.successResponse({'games': result})


@app.route('/games/delete/<version>/', methods=['DELETE'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def gameDelete(version):
	"""
	Deletes game and supporting data.

	Arguments:
	key -- the key for the game
	"""
	backend = content.Content()
	success = backend.deleteGame(request.json['key'])
	
	if success:
		return rest.successResponse({'deleted': success>0})
	return rest.errorResponse(errors.GameKeyDoesNotExist)


@app.route('/games/get/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def gameGet(version):
	"""
	Gets information about game.

	Arguments:
	key -- the key for the game
	"""
	backend = content.Content()	
	game = backend.getGame(request.json['key'])
	if game:
		return rest.successResponse(game.as_dict())
	
	return rest.errorResponse(errors.GameKeyDoesNotExist)


@app.route('/games/update/<version>/', methods=['PUT'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def gameUpdate(version):
	"""
	Updates game information.

	Arguments:
	key -- the game key
	name -- (optional) the name of the game 

	"""
	backend = content.Content()

	game = backend.setGame(request.json['key'], request.json)

	if game:
		return rest.successResponse(game.as_dict())
	return rest.errorResponse(errors.GameKeyDoesNotExist)


@app.route('/currencies/get/<version>/', methods=['GET'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def currencyGet(version):
	"""
	Get currency for the specified game.

	Arguments:
	key -- the game key
	"""
	backend = content.Content()

	currency = backend.getCurrency(request.json['key'])
	if currency:
		return rest.successResponse(currency.as_dict())
	return rest.errorResponse(errors.GameKeyDoesNotExist)


@app.route('/currencies/update/<version>/', methods=['PUT'])
@rest.userAuthenticate(secretLookup=lambda s: config.UserSecret)
def currencyUpdate(version):
	"""
	Updates a single currency name for the game specified.

	Arguments:
	key -- the game key
	name1 to name8 -- name of currencies in the game
	"""

	backend = content.Content()

	currency = backend.setCurrency(request.json['key'], request.json)
	if currency:
		return rest.successResponse(currency.as_dict())
	return rest.errorResponse(errors.GameKeyDoesNotExist)


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
	return rest.errorResponse(errors.GameKeyDoesNotExist)


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
	return rest.errorResponse(errors.GameKeyDoesNotExist)


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


@app.route('/update/<version>/', methods=['POST'])
@rest.gameAuthenticate(secretLookup=content.Content().getGameSecret)
def update(version):

	theStorage = storage.getDefaultStorage()
	backend = content.Content()

	# Check minimum number of keys required in JSON update
	if extras.keysInDict(request.json, ['player', 'events']) == False:
		return rest.errorResponse(errors.GameUpdateIncomplete)

	# Events must have at least one item
	if len(request.json['events']) == 0:
		return rest.errorResponse(errors.GameUpdateMissingEvents)
	
	# Event has progress
	if 'progress' not in request.json['events'][-1]:
		return rest.errorResponse(errors.GameUpdateMissingEvents)
	
	# Try getting price engine
	try:
		prices = backend.getPricingEngine(request.json['gondola-application'])
	except pricing.GameNotFoundException:
		return rest.errorResponse(errors.GameKeyDoesNotExist)

	# Try getting price for player + progress
	try:
		playerPrices = prices.getPrices(request.json['player'], request.json['events'][-1]['progress'])
	except pricing.NoPricingForGroup:
		return rest.errorResponse(errors.GameHasNoPriceForPlayer)

	# Save update
	key = '%s-%s-%s.json'%(request.json['gondola-application'], extras.datetimeStamp(), request.json['player'])
	theStorage.save(key, json.dumps(request.json))


# {
# 	gondola-application: game key
# 	player: player UUID
# 	events: [
# 		{
# 			name: event name
# 			time: UTC time
# 			attributes: [8 string, 8 float]
# 			progress: [8 string, 24 float values]
# 		}
# 	]
# }

	return rest.successResponse(playerPrices)

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