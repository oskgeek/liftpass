import service.service as service
import config

from core import factory
import util.debug as debug
import util.rest as rest
import service.sdk.errors as errors
import engine.pricing.pricing as pricing

from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)


@app.route('/update/<version>/', methods=['POST'])
def update(version):

	storage = factory.getStorage()
	content = factory.getContent()

	# Check minimum number of keys required in JSON update
	if service.keysInDict(request.json, ['application', 'player', 'events']) == False:
		return rest.errorResponse(errors.GameUpdateIncomplete)

	# Events must have at least one item
	if len(request.json['events']) == 0:
		return res.errorResponse(errors.GameUpdateMissingEvents)
	
	# Event has progress
	if 'progress' not in request.json['events'][-1]:
		return res.errorResponse(errors.GameUpdateMissingEvents)
	
	try:
		prices = content.getPricingEngine(request.json['application'])
	except pricing.GameNotFoundException:
		return rest.errorResponse(errors.GameKeyDoesNotExist)


	try:
		playerPrices = prices.getPrices(request.json['player'], request.json['events'][-1]['progress'])
	except pricing.NoPricingForGroup:
		return rest.errorResponse(errors.GameHasNoPriceForPlayer)



# {
# 	application: game key
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




def start():
	global app
	app.run(debug=config.SDKDebug, port=config.SDKPort)

def getApp():
	global app
	return app