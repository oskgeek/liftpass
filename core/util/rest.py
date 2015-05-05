from flask import jsonify
from flask import request
from flask import Response
import hmac
import hashlib
from functools import wraps
from functools import update_wrapper
import time
import json

import core.util.debug as debug
import core.util.extras as extras


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

def buildResponse(content, secret, application=None):
	if isinstance(content, dict) == False:
		return content

	data = {}
	status = 200
	
	if 'status' in content:
		data = {'error': content['message']}
		status = content['status']
	else:
		data = content
	
	if application:
		data['liftpass-application'] = application	

	data['liftpass-time'] = round(time.time())
	data = extras.toJSON(data)

	response = Response(data, status, {'content-type':'application/json'})
	if secret:
		digest = hmac.new(secret, data.encode('utf-8'), hashlib.sha256).hexdigest()
		response.headers['liftpass-hash'] = digest

	response.status_code = status

	return response


def userAuthenticate(secretLookup):
	def decorator(f): 
		def aux(*args, **kwargs):
			# If JSON not specified
			if request.json == None:
				return buildResponse({'status': ERROR_BAD_REQUEST, 'message': 'No JSON body specified with request'}, secret)

			# JSON must include time and user key
			if not all(map(lambda k: k in request.json, ['liftpass-time', 'liftpass-user'])):
				return buildResponse({'status': ERROR_UNAUTHORIZED, 'message':'JSON missing liftpass-time and/or liftpass-user keys'}, secret)

			# HTTP header must include hash for all requests
			if 'liftpass-hash' not in request.headers:
				return buildResponse({'status': ERROR_UNAUTHORIZED, 'message':'HTTP request missing liftpass-hash in header'}, secret)

			secret = secretLookup(request.json['liftpass-user'])
			digest = hmac.new(secret, request.get_data(), hashlib.sha256).hexdigest()
			
			if digest != request.headers['liftpass-hash']:
				return buildResponse({'status': ERROR_UNAUTHORIZED, 'message':'Failed to authenticate'}, secret)
			
			return buildResponse(f(*args, **kwargs), secret)
		return update_wrapper(aux, f)
	return decorator


def applicationAuthenticate(secretLookup):
	def decorator(f): 
		def aux(*args, **kwargs):

			# JSON must include time and user key
			if not all(map(lambda k: k in request.json, ['liftpass-time', 'liftpass-application'])):
				return buildResponse({'status': ERROR_UNAUTHORIZED, 'message':'JSON missing liftpass-time and/or liftpass-application keys'}, secret)

			# HTTP header must include hash for all requests
			if 'liftpass-hash' not in request.headers:
				return buildResponse({'status': ERROR_UNAUTHORIZED, 'message':'HTTP request missing liftpass-hash in header'}, secret)

			secret = secretLookup(request.json['liftpass-application'])
			if secret == None:
				return buildResponse({'status': ERROR_UNAUTHORIZED, 'message':'Application key not valid'}, secret)

			secret = secret.encode('utf-8')	
			digest = hmac.new(secret, request.get_data(), hashlib.sha256).hexdigest()
			
			if digest != request.headers['liftpass-hash']:
				return buildResponse({'status': ERROR_UNAUTHORIZED, 'message':'Failed to authenticate'}, secret)
			
			return buildResponse(f(*args, **kwargs), secret, request.json['liftpass-application'])
		return update_wrapper(aux, f)
	return decorator