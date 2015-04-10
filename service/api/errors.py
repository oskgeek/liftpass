import util.rest as rest

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