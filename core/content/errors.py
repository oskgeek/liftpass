import core.util.rest as rest

RequestMissingArguments = {
	'message': 'Request missing arguments',
	'status': rest.ERROR_BAD_REQUEST
}

FailedToAuthenticate = {
	'message': 'Request failed to be authenticated',
	'status': rest.ERROR_UNAUTHORIZED
}

GameKeyDoesNotExist =  {
	'message': 'Game key does not exist',
	'status': rest.ERROR_BAD_REQUEST
}

GoodKeyDoesNotExist =  {
	'message': 'Good key does not exist',
	'status': rest.ERROR_BAD_REQUEST
}

PricesKeyDoesNotExist = {
	'message': 'Prices key does not exist',
	'status': rest.ERROR_BAD_REQUEST
}

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