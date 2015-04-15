import os
import sys

import config


if len(sys.argv) < 3:
	print(' - manage API start/test')

elif sys.argv[1] == 'API':
	if sys.argv[2] == 'start':
		import core.content.main as main
		main.start()
	else:
		print('Error: command not found')
elif sys.argv[1] == 'analytics':
	if sys.argv[2] == 'update':
		import core.analytics.analytics as analytics
		analytics.Analytics().processUpdates()
elif sys.argv[1] == 'test':
	if sys.argv[2] == 'API':
		import tests.content
	elif sys.argv[2] == 'pricing':
		import tests.pricing
	elif sys.argv[2] == 'all':
		import tests.content
		import tests.pricing