import os
import sys

import config


if len(sys.argv) < 3:
	print(' - manage API start')
	print(' - manage analytics update')
	print(' - manage dashboard start')
	print(' - manage test API/pricing/analytics/all/coverage')

elif sys.argv[1] == 'API':
	if sys.argv[2] == 'start':
		import core.api.main as main
		main.start()
elif sys.argv[1] == 'analytics':
	if sys.argv[2] == 'update':
		import core.analytics.analytics as analytics
		analytics.Analytics().processUpdates()
elif sys.argv[1] == 'dashboard':
	if sys.argv[2] == 'start':
		import core.dashboard.main as main
		main.start()
elif sys.argv[1] == 'test':
	if sys.argv[2] == 'API':
		import tests.content
	elif sys.argv[2] == 'pricing':
		import tests.pricing
	elif sys.argv[2] == 'analytics':
		import tests.analytics
	elif sys.argv[2] == 'terminal':
		import tests.terminal
	elif sys.argv[2] == 'all':
		import tests.content
		import tests.pricing
		import tests.analytics
		import tests.terminal
	elif sys.argv[2] == 'coverage':
		os.system('coverage-3.4 run manage.py test all')
		os.system('coverage-3.4 report')