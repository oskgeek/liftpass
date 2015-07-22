import os
import sys

try:
	import config
except:
	pass

if len(sys.argv) < 2:
	print(' - manage API start')
	print(' - manage content flush/create')
	print(' - manage analytics update')
	print(' - manage dashboard start')
	print(' - manage demo build')
	print(' - manage configure')
	print(' - manage test API/pricing/analytics/all/coverage')
elif sys.argv[1] == 'API':
	if len(sys.argv) == 5:
		config.APIServer['address'] = sys.argv[3]
		config.APIServer['port'] = int(sys.argv[4])
	if sys.argv[2] == 'start':
		import core.api.main as main
		main.start()
elif sys.argv[1] == 'content':
	if sys.argv[2] == 'flush':
		import core.content.models as models
		models.flush()
	elif sys.argv[2] == 'create':
		import core.content.models as models
		models.create()
elif sys.argv[1] == 'analytics':
	if sys.argv[2] == 'update':
		import core.analytics.analytics as analytics

		limit = None
		if len(sys.argv) > 4:
			processors = int(sys.argv[3])
			limit = int(sys.argv[4])
			analytics.Analytics().processUpdates(processors, limit)
		else:
			analytics.Analytics().processUpdates()
			
elif sys.argv[1] == 'dashboard':
	if sys.argv[2] == 'start':
		import core.dashboard.main as main
		main.start()
elif sys.argv[1] == 'demo':
	answer = input('Are you sure you want to setup demo? All data will be lost. [y/n]')
	answer = answer.lower().strip()
	if  answer == 'y':
		import core.demo as demo
		demo.start()
	elif answer == 'n':
		print('Demo build aborted.')
	else:
		print('Nevermind - incorrect answer. No demo will be built.')
elif sys.argv[1] == 'configure':
	import core.configure as configure
	configure.run()
elif sys.argv[1] == 'test':
	if sys.argv[2] == 'content':
		import tests.content
	elif sys.argv[2] == 'pricing':
		import tests.pricing
	elif sys.argv[2] == 'analytics':
		import tests.analytics
	elif sys.argv[2] == 'terminal':
		import tests.terminal
	elif sys.argv[2] == 'stress':
		import tests.stress
		if len(sys.argv) > 3 and sys.argv[3] == 'analyze':
			tests.stress.analyze()
		else:
			tests.stress.run()
	elif sys.argv[2] == 'all':
		import tests.content
		import tests.pricing
		import tests.analytics
		import tests.terminal
	elif sys.argv[2] == 'coverage':
		os.system('coverage-3.4 run manage.py test all')
		os.system('coverage-3.4 report')