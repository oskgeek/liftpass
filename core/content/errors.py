import core.util.rest as rest

RequestMissingArguments = {
	'message': 'Request missing arguments',
	'status': rest.ERROR_BAD_REQUEST
}

FailedToAuthenticate = {
	'message': 'Request failed to be authenticated',
	'status': rest.ERROR_UNAUTHORIZED
}

ApplicationKeyDoesNotExist =  {
	'message': 'Application key does not exist',
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

ApplicationKeyDoesNotExist =  {
	'message': 'Application key does not exist',
	'status': rest.ERROR_BAD_REQUEST
}

ApplicationUpdateIncomplete = {
	'message': 'JSON game update is incomplete',
	'status': rest.ERROR_BAD_REQUEST
}

ApplicationUpdateMissingEvents = {
	'message': 'JSON game update must have at least one event',
	'status': rest.ERROR_BAD_REQUEST
}

ApplicationHasNoPriceForUser = {
	'message': 'Application has no specified prices for user/group',
	'status': rest.ERROR_BAD_REQUEST
}