import util.rest as rest


GameKeyDoesNotExist =  {
	'message': 'Game key does not exist',
	'status': rest.ERROR_BAD_REQUEST
}

GameUpdateIncomplete = {
	'message': 'JSON game update is incomplete',
	'status': rest.ERROR_BAD_REQUEST
}

GameUpdateMissingEvents = {
	'message': 'JSON game update must have at least one event',
	'status': rest.ERROR_BAD_REQUEST
}

GameHasNoPriceForPlayer = {
	'message': 'Game has no specified prices for player/group',
	'status': rest.ERROR_BAD_REQUEST
}