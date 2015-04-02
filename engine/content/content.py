import uuid

import config

from engine.content import models
from engine.pricing import pricing
from util import debug

class Content:


	def __init__(self):
		debug.log('[%s] Init'%self)


	def addGame(self, name):	
		session = models.getSession()
		
		game = models.Game(name=name)
		
		currencies = models.Currencies(game=game)
		abtest = models.ABTest(game=game)
		metrics = models.Metrics(game=game)

		session.add(game)
		session.add(currencies)
		session.add(abtest)
		session.add(metrics)
		session.commit()

		return game

	def getGames(self):
		return models.getSession().query(models.Game).all()

	def getGame(self, game_key):
		return models.getSession().query(models.Game).filter_by(key=game_key).first()

	def deleteGame(self, game_key):
		session = models.getSession()
		res = session.query(models.Game).filter_by(key=game_key).delete()
		session.commit()
		return res

	def setGame(self, game_key, json):
		session = models.getSession()
		game = session.query(models.Game).filter_by(key=game_key).first()
		if game:
			models.updateObjectWithJSON(game, json, ['key'])
			session.commit()
		return game

	def getCurrency(self, game_key):
		session = models.getSession()
		return session.query(models.Currencies).join(models.Game).filter_by(key=game_key).first()

	def setCurrency(self, game_key, json):
		session = models.getSession()
		currencies = session.query(models.Currencies).join(models.Game).filter_by(key=game_key).first()

		if currencies:
			models.updateObjectWithJSON(currencies, json, ['key'])
			session.commit()
		return currencies

	def addGood(self, game_key, name):
		session = models.getSession()
		

		game = session.query(models.Game).filter_by(key = game_key).first()
	
		good = models.Good(name=name, game_key=game.key)
		
		session.add(good)
		session.commit()

		return good

	def getGood(self, key):
		session = models.getSession()
		return session.query(models.Good).filter_by(key = key).first()

	def getGoods(self, game_key):
		session = models.getSession()
		return session.query(models.Good).join(models.Game).filter(models.Game.key == game_key).all()

	def deleteGood(self, good_key):
		session = models.getSession()
		res = session.query(models.Good).filter_by(key=good_key).delete()
		session.commit()
		return res

	def updateGood(self, good_key, json):
		session = models.getSession()
		good = session.query(models.Good).filter_by(key=good_key).first()
		if good:
			models.updateObjectWithJSON(good, json, ['key', 'game_key'])
			session.commit()
		return good

	def getABTest(self, game_key):
		session = models.getSession()
		abtest = session.query(models.ABTest).join(models.Game).filter(models.Game.key == game_key).first()
		return abtest

	def setABTest(self, game_key, json):
		session = models.getSession()

		abtest = session.query(models.ABTest).join(models.Game).filter(models.Game.key == game_key).first()

		if abtest:
			# Check price foreign keys manually
			for prices in ['dynamicPrices_key', 'staticPrices_key']:
				if prices in json and json[prices] != None:
					count = session.query(models.Prices).join(models.Game).filter(models.Game.key == abtest.game_key).filter(models.Prices.key==json[prices]).count()
					if count == 1:
						pass
					else:
						debug.error('Prices key is not valid')
						del json[prices]

			models.updateObjectWithJSON(abtest, json, ['key'])
			session.commit()
		return abtest 

	def getMetrics(self, game_key):
		session = models.getSession()
		return session.query(models.Metrics).join(models.Game).filter(models.Game.key == game_key).first()

	def setMetrics(self, game_key, json):
		session = models.getSession()

		metrics = session.query(models.Metrics).join(models.Game).filter(models.Game.key == game_key).first()
		if metrics:
			models.updateObjectWithJSON(metrics, json, ['key'])
			session.commit()
		return metrics 

	def getPrices(self, game_key):
		session = models.getSession()
		return session.query(models.Prices).join(models.Game).filter(models.Game.key == game_key).all()

	def getPrice(self, prices_key):
		session = models.getSession()
		return session.query(models.Prices).filter_by(key = prices_key).first()

	def getPricingEngine(self, game_key):
		return pricing.PricingEngine(game_key)


	def deletePrices(self, prices_key):
		session = models.getSession()

		# Check if prices is currently used
		count =  session.query(models.ABTest).join(models.Game).filter(models.Game.key == models.ABTest.game_key).filter(models.ABTest.dynamicPrices_key == prices_key).count()
		if count != 0:
			debug.error("Prices cannot be deleted while still active")
			return 0
		
		count =  session.query(models.ABTest).join(models.Game).filter(models.Game.key == models.ABTest.game_key).filter(models.ABTest.staticPrices_key == prices_key).count()
		if count != 0:
			debug.error("Prices cannot be deleted while still active")
			return 0

		res = session.query(models.Prices).filter_by(key = prices_key).delete()
		session.commit()
		return res

	def addPrices(self, game_key, engine, data, path):
		session = models.getSession()
		prices = models.Prices(game_key = game_key, engine=engine, data=data, path=path)
		session.add(prices)
		session.commit()
		return prices

	def __repr__(self):
		return 'Content'