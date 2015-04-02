import os
import sys

import config


if len(sys.argv) < 3:
	print(' - manage SDK')
	print(' - manage API start/test')

elif sys.argv[1] == 'SDK':
	if sys.argv[2] == 'start':
		import service.sdk.main as SDKService
		SDKService.start()
	elif sys.argv[2] == 'test':
		import tests.sdk
	else:
		print('Error command not found')

elif sys.argv[1] == 'API':
	if sys.argv[2] == 'start':
		import service.api.main as APIService
		APIService.start()
	elif sys.argv[2] == 'test':
		import tests.content
	else:
		print('Error: command not found')
elif sys.argv[1] == 'test':
	if sys.argv[2] == 'API':
		import tests.content
	elif sys.argv[2] == 'pricing':
		import tests.pricing