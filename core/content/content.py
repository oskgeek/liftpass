import uuid

import config

import core.content.models as models
import core.pricing.pricing as pricing
import core.util.debug as debug


def cacheObject(obj):
	list(map(lambda i: getattr(obj, i), dir(obj)))
	return obj

def cacheObjects(objs):
	list(map(lambda o: cacheObject(o), objs))
	return objs

class Content:

	def addApplication(self, name):	
		session = models.getSession()
		
		application = models.Application(name=name)
		
		currencies = models.Currencies(application=application)
		abtest = models.ABTest(application=application)
		metrics = models.Metrics(application=application)

		session.add(application)
		session.add(currencies)
		session.add(abtest)
		session.add(metrics)
		session.commit()

		cacheObject(application)
		session.close()
		
		return application


	def getApplications(self):
		session = models.getSession()
		applications = session.query(models.Application).all()

		cacheObjects(applications)
		session.close()

		return applications

	def getApplication(self, application_key):
		session = models.getSession()
		app = session.query(models.Application).filter_by(key=application_key).first()

		cacheObject(app)
		session.close()
		
		return app

	def getApplicationExists(self, application_key):
		session = models.getSession()
		app = session.query(models.Application).filter_by(key=application_key).count()

		session.close()
		
		return app

	def getApplicationWithName(self, name):
		session = models.getSession()
		app = session.query(models.Application).filter_by(name=name).first()		
		
		cacheObject(app)
		session.close()
		
		return app

	def deleteApplication(self, application_key):
		session = models.getSession()
		res = session.query(models.Application).filter_by(key=application_key).delete()
		session.commit()
		
		session.close()

		return res

	def setApplication(self, application_key, json):
		session = models.getSession()
		application = session.query(models.Application).filter_by(key=application_key).first()
		if application:
			models.updateObjectWithJSON(application, json, ['key'])
			session.commit()

		cacheObject(application)
		session.close()
		
		return application

	def getCurrency(self, application_key):
		session = models.getSession()
		currency = session.query(models.Currencies).join(models.Application).filter_by(key=application_key).first()
		
		cacheObject(currency)
		session.close()

		return currency

	def setCurrency(self, application_key, json):
		session = models.getSession()
		currencies = session.query(models.Currencies).join(models.Application).filter_by(key=application_key).first()

		if currencies:
			models.updateObjectWithJSON(currencies, json, ['key'])
			session.commit()

		cacheObject(currencies)
		session.close()

		return currencies

	def addGood(self, application_key, name):
		session = models.getSession()
		

		application = session.query(models.Application).filter_by(key = application_key).first()
	
		good = models.Good(name=name, application_key=application.key)
		
		session.add(good)
		session.commit()

		cacheObject(good)
		session.close()

		return good

	def getGood(self, key):
		session = models.getSession()
		good = session.query(models.Good).filter_by(key = key).first()
		
		cacheObject(good)
		session.close()

		return good

	def getGoods(self, application_key):
		session = models.getSession()
		goods = session.query(models.Good).join(models.Application).filter(models.Application.key == application_key).all()
		
		cacheObjects(goods)
		session.close()

		return goods

	def deleteGood(self, good_key):
		session = models.getSession()
		res = session.query(models.Good).filter_by(key=good_key).delete()
		session.commit()

		
		session.close()
		
		return res

	def updateGood(self, good_key, json):
		session = models.getSession()
		good = session.query(models.Good).filter_by(key=good_key).first()
		if good:
			models.updateObjectWithJSON(good, json, ['key', 'application_key'])
			session.commit()

		cacheObject(good)
		session.close()

		return good

	def getABTest(self, application_key):
		session = models.getSession()

		abtests = session.query(models.ABTest).join(models.Application).filter(models.Application.key == application_key).order_by(models.ABTest.id.desc()).limit(1).all()
		
		if len(abtests) == 1:
			
			cacheObject(abtests[0])
			session.close()
			
			return abtests[0]

		session.close()		
		return None

	def setABTest(self, application_key, json):
		session = models.getSession()

		abtest = self.getABTest(application_key)

		if abtest:

			newABTest = models.ABTest()
			newABTest.application_key = abtest.application_key
			newABTest.countryWhiteList = abtest.countryWhiteList
			newABTest.countryBlackList = abtest.countryBlackList
			newABTest.modulus = abtest.modulus
			newABTest.modulusLimit = abtest.modulusLimit
			newABTest.groupAPrices_key = abtest.groupAPrices_key
			newABTest.groupBPrices_key = abtest.groupBPrices_key

			# Check price foreign keys manually
			for prices in ['groupAPrices_key', 'groupBPrices_key']:
				if prices in json and json[prices] != None:
					count = session.query(models.Prices).join(models.Application).filter(models.Application.key == newABTest.application_key).filter(models.Prices.key==json[prices]).count()
					if count == 1:
						pass
					else:
						del json[prices]
			
			models.updateObjectWithJSON(newABTest, json, ['key'])
			session.add(newABTest)
			session.commit()

			cacheObject(newABTest)
			
		session.close()

		return newABTest 

	def getMetrics(self, application_key):
		session = models.getSession()
		metrics = session.query(models.Metrics).join(models.Application).filter(models.Application.key == application_key).first()
		if metrics:
			cacheObject(metrics)
		session.close()
		
		return metrics

	def setMetrics(self, application_key, json):
		session = models.getSession()

		metrics = session.query(models.Metrics).join(models.Application).filter(models.Application.key == application_key).first()
		if metrics:
			models.updateObjectWithJSON(metrics, json, ['key'])
			session.commit()
			cacheObject(metrics)
		
		session.close()

		return metrics 

	def getPrices(self, application_key):
		session = models.getSession()
		prices = session.query(models.Prices).join(models.Application).filter(models.Application.key == application_key).all()
		
		cacheObjects(prices)
		session.close()
		
		return prices

	def getPrice(self, prices_key):
		session = models.getSession()
		price = session.query(models.Prices).filter_by(key = prices_key).first()
		
		cacheObject(price)
		session.close()
		
		return price

	def getPricingEngine(self, application_key):
		return pricing.PricingEngine.getApplicationPricing(application_key)


	def deletePrices(self, prices_key):
		session = models.getSession()

		prices = session.query(models.Prices).filter_by(key = prices_key).first()
		prices.data = None
		prices.path = None
		prices.deleted = True

		abtest = self.getABTest(prices.application_key)
		if abtest.groupAPrices_key == prices_key and abtest.groupBPrices_key != prices_key:
			self.setABTest(prices.application_key, {'groupAPrices_key': None})
		elif abtest.groupAPrices_key != prices_key and abtest.groupBPrices_key == prices_key:
			self.setABTest(prices.application_key, {'groupBPrices_key': None})
		elif abtest.groupAPrices_key == prices_key and abtest.groupBPrices_key == prices_key:
			self.setABTest(prices.application_key, {'groupAPrices_key': None, 'groupBPrices_key': None})

		session.commit()
		
		session.close()

		return True

	def addPrices(self, application_key, engine, data, path):
		session = models.getSession()
		prices = models.Prices(application_key = application_key, engine=engine, data=data, path=path)
		pricing.PricingEngine.validate(prices)
		session.add(prices)
		session.commit()

		cacheObject(prices)
		session.close()
		
		return prices


	def getApplicationSecret(self, application_key):
		session = models.getSession()
		application = session.query(models.Application).filter_by(key = application_key).first()
	
		if application != None:
			session.close()
			return application.secret

		session.close()
		return None
		

	def __repr__(self):
		return 'Content'