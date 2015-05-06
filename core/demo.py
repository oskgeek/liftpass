import json

import core.content.content as content



def start():
	theContent = content.Content()

	# Delete existing apps
	apps = theContent.getApplications()
	for app in apps:
		theContent.deleteApplication(app.key)

	# Create demo game
	game = theContent.addApplication('Monopoly')


	goods = {
		'com.monopoly.mediterranean': 60,
		'com.monopoly.baltic': 60,
		'com.monopoly.oriental': 100, 
		'com.monopoly.vermont': 100,
		'com.monopoly.connecticut': 120,
		'com.monopoly.charles': 140,
		'com.monopoly.states': 140,
		'com.monopoly.virginia': 160,
		'com.monopoly.james': 180,
		'com.monopoly.tennessee': 180,
		'com.monopoly.newyork': 200,
		'com.monopoly.kentucky': 220,
		'com.monopoly.indiana': 220,
		'com.monopoly.illinois': 240,
		'com.monopoly.atlantic': 260,
		'com.monopoly.ventnor': 260,
		'com.monopoly.marvin': 280,
		'com.monopoly.pacific': 300,
		'com.monopoly.northcarolina': 300,
		'com.monopoly.pennsylvania': 320,
		'com.monopoly.parkplace': 350,
		'com.monopoly.boardwalk': 400,
		'com.monopoly.electric': 150,
		'com.monopoly.water': 150,
		'com.monopoly.readingrailroad': 200,
		'com.monopoly.pennrailroad': 200,
		'com.monopoly.borailroad': 200,
		'com.monopoly.shortlinerailroad': 200
	}
	
	# Add goods to game
	for good in goods:
		theContent.addGood(game.key, good)

	# Set currencies
	theContent.setCurrency(game.key, {'currency1': 'dollar'})

	# Set metrics
	theContent.setMetrics(game.key, {
		'metricString1': 'Device',
		'metricString2': 'OS',
		'metricString3': 'OS Version',
		'metricString4': 'Language',
		'metricNumber1': 'Rolls',
		'metricNumber2': 'Total earned dollars',
		'metricNumber3': 'Total spent dollars',
		'metricNumber4': 'Total purchases',
		'metricNumber5': 'Times in Jail',
		'metricNumber6': 'Total Rent Paid',
		'metricNumber7': 'Total Rent Earned',
	})

	# Set prices
	pricesA = dict(map(lambda good: (good, int(goods[good]*1.0)), goods))
	pricesA = theContent.addPrices(game.key, 'JSON', json.dumps(pricesA), None)

	pricesB = dict(map(lambda good: (good, int(goods[good]*2.5)), goods))
	pricesB = theContent.addPrices(game.key, 'JSON', json.dumps(pricesB), None)

	# Set A/B test
	theContent.setABTest(game.key, {
		'groupAPrices_key': pricesB.key,
		'groupBPrices_key': pricesA.key,
		'modulus': 5,
		'modulusLimit': 3,
	})

