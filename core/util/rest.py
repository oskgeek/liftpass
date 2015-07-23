from flask import jsonify
from flask import request
from flask import Response
import hmac
import hashlib
from functools import wraps
from functools import update_wrapper
import time
import json
import base64
import datetime

import core.util.debug as debug
import core.util.extras as extras
import core.monitoring as monitor


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

def cleanupValues():
	for k in request.values:
		try:
			request.values[k] = request.values[k].strip()
		except:
			pass


def userAuthenticate(secretLookup):
	def decorator(f): 
		def aux(*args, **kwargs):
			
			message = request.get_data()
			if 'json' in request.args:
				message = base64.b64decode(request.args['json'])
				request.values = json.loads(message.decode('utf-8'))
			else: 
				request.values = request.json
			cleanupValues()

			# If JSON not specified
			if request.values == None:
				return buildResponse({'status': ERROR_BAD_REQUEST, 'message': 'No JSON body specified with request'}, secret)

			# JSON must include time and user key
			if not all(map(lambda k: k in request.values, ['liftpass-time', 'liftpass-user'])):
				return buildResponse({'status': ERROR_UNAUTHORIZED, 'message':'JSON missing liftpass-time and/or liftpass-user keys'}, secret)

			# HTTP header must include hash for all requests
			if 'liftpass-hash' not in request.headers:
				return buildResponse({'status': ERROR_UNAUTHORIZED, 'message':'HTTP request missing liftpass-hash in header'}, secret)

			secret = secretLookup(request.values['liftpass-user'])
			digest = hmac.new(secret, message, hashlib.sha256).hexdigest()
			
			if digest != request.headers['liftpass-hash']:
				return buildResponse({'status': ERROR_UNAUTHORIZED, 'message':'Failed to authenticate'}, secret)
			
			return buildResponse(f(*args, **kwargs), secret)
		return update_wrapper(aux, f)
	return decorator


def applicationAuthenticate(secretLookup):
	def decorator(f): 
		def aux(*args, **kwargs):

			monitor.getMonitor().count('ApplicationRequestCount')
			
			debug.log('%s %s %s'%(request.method, request.path, request.environ.get('HTTP_X_REAL_IP')))

			with monitor.getMonitor().time('ApplicationValidateTime'):
				
				# All user input goes to the values field of the request
				message = request.get_data()
				if 'json' in request.args:
					message = base64.b64decode(request.args['json'])
					request.values = json.loads(message.decode('utf-8'))
				elif len(request.json):
					request.values = request.json


				# JSON must include time and user key
				if not all(map(lambda k: k in request.values, ['liftpass-time', 'liftpass-application'])):
					monitor.getMonitor().count('ApplicationRequestMissingHeaderCount')
					return buildResponse({'status': ERROR_UNAUTHORIZED, 'message':'JSON missing liftpass-time and/or liftpass-application keys'}, secret)

				# HTTP header must include hash for all requests
				if 'liftpass-hash' not in request.headers:
					monitor.getMonitor().count('ApplicationRequestMissingHashCount')
					return buildResponse({'status': ERROR_UNAUTHORIZED, 'message':'HTTP request missing liftpass-hash in header'}, secret)

				secret = secretLookup(request.values['liftpass-application'])
				if secret == None:
					monitor.getMonitor().count('ApplicationRequestApplicationNotFoundCount')
					return buildResponse({'status': ERROR_UNAUTHORIZED, 'message':'Application key not valid'}, secret)

				secret = secret.encode('utf-8')	
				digest = hmac.new(secret, message, hashlib.sha256).hexdigest()
				
				if digest != request.headers['liftpass-hash']:
					monitor.getMonitor().count('ApplicationRequestBadHashCount')
					return buildResponse({'status': ERROR_UNAUTHORIZED, 'message':'Failed to authenticate'}, secret)
				
				with monitor.getMonitor().time('ApplicationProcessResponseTime'):
					return buildResponse(f(*args, **kwargs), secret, request.values['liftpass-application'])
		return update_wrapper(aux, f)
	return decorator
