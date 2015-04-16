from flask import jsonify
from flask import request
from flask import Response
import hmac
import hashlib
from functools import wraps
from functools import update_wrapper

import core.util.debug as debug


ERROR_BAD_REQUEST = 400
ERROR_UNAUTHORIZED = 401
ERROR_FORBIDDEN = 403
ERROR_NOT_MODIFIED = 304
ERROR_NOT_FOUND = 404

SUCCESS_OK = 200
SUCCESS_CREATED = 201


def streamResponse(stream):
	return Response(stream(), mimetype='application/json')

def successResponse(data, status=200):
	res = jsonify(data)
	res.status_code = status
	return res

def errorResponse(error):
	res = jsonify({'error': error['message']})
	res.status_code = error['status']
	return res

def userAuthenticate(secretLookup):
	def decorator(f): 
		def aux(*args, **kwargs):
			# If JSON not specified
			if request.json == None:
				return errorResponse({'status': ERROR_BAD_REQUEST, 'message': 'No JSON body specified with request'})

			# JSON must include time and user key
			if not all(map(lambda k: k in request.json, ['gondola-time', 'gondola-user'])):
				return errorResponse({'status': ERROR_UNAUTHORIZED, 'message':'JSON missing gondola-time and/or gondola-user keys'})

			# HTTP header must include hash for all requests
			if 'gondola-hash' not in request.headers:
				return errorResponse({'status': ERROR_UNAUTHORIZED, 'message':'HTTP request missing gondola-hash in header'})

			secret = secretLookup(request.json['gondola-user'])
			digest = hmac.new(secret, request.get_data(), hashlib.sha256).hexdigest()
			
			debug.error(request.get_data().decode('utf-8'))

			if digest != request.headers['gondola-hash']:
				debug.error('Hash not valid: %s %s'%(digest, request.headers['gondola-hash']))
				return errorResponse({'status': ERROR_UNAUTHORIZED, 'message':'Failed to authenticate'})
			
			return f(*args, **kwargs)
		return update_wrapper(aux, f)
	return decorator


def applicationAuthenticate(secretLookup):
	def decorator(f): 
		def aux(*args, **kwargs):

			# JSON must include time and user key
			if not all(map(lambda k: k in request.json, ['gondola-time', 'gondola-application'])):
				return errorResponse({'status': ERROR_UNAUTHORIZED, 'message':'JSON missing gondola-time and/or gondola-application keys'})

			# HTTP header must include hash for all requests
			if 'gondola-hash' not in request.headers:
				return errorResponse({'status': ERROR_UNAUTHORIZED, 'message':'HTTP request missing gondola-hash in header'})

			secret = secretLookup(request.json['gondola-application'])
			if secret == None:
				return errorResponse({'status': ERROR_UNAUTHORIZED, 'message':'Application key not valid'})

			secret = secret.encode('utf-8')	
			digest = hmac.new(secret, request.get_data(), hashlib.sha256).hexdigest()
			
			if digest != request.headers['gondola-hash']:
				return errorResponse({'status': ERROR_UNAUTHORIZED, 'message':'Failed to authenticate'})
			
			return f(*args, **kwargs)
		return update_wrapper(aux, f)
	return decorator