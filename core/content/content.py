import uuid

import config

import core.content.models as models
import core.pricing.pricing as pricing
import core.util.debug as debug


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
		
		return application

	def getApplications(self):
		return models.getSession().query(models.Application).all()

	def getApplication(self, application_key):
		return models.getSession().query(models.Application).filter_by(key=application_key).first()

	def deleteApplication(self, application_key):
		session = models.getSession()
		res = session.query(models.Application).filter_by(key=application_key).delete()
		session.commit()
		return res

	def setApplication(self, application_key, json):
		session = models.getSession()
		application = session.query(models.Application).filter_by(key=application_key).first()
		if application:
			models.updateObjectWithJSON(application, json, ['key'])
			session.commit()
		return application

	def getCurrency(self, application_key):
		session = models.getSession()
		return session.query(models.Currencies).join(models.Application).filter_by(key=application_key).first()

	def setCurrency(self, application_key, json):
		session = models.getSession()
		currencies = session.query(models.Currencies).join(models.Application).filter_by(key=application_key).first()

		if currencies:
			models.updateObjectWithJSON(currencies, json, ['key'])
			session.commit()
		return currencies

	def addGood(self, application_key, name):
		session = models.getSession()
		

		application = session.query(models.Application).filter_by(key = application_key).first()
	
		good = models.Good(name=name, application_key=application.key)
		
		session.add(good)
		session.commit()

		return good

	def getGood(self, key):
		session = models.getSession()
		return session.query(models.Good).filter_by(key = key).first()

	def getGoods(self, application_key):
		session = models.getSession()
		return session.query(models.Good).join(models.Application).filter(models.Application.key == application_key).all()

	def deleteGood(self, good_key):
		session = models.getSession()
		res = session.query(models.Good).filter_by(key=good_key).delete()
		session.commit()
		return res

	def updateGood(self, good_key, json):
		session = models.getSession()
		good = session.query(models.Good).filter_by(key=good_key).first()
		if good:
			models.updateObjectWithJSON(good, json, ['key', 'application_key'])
			session.commit()
		return good

	def getABTest(self, application_key):
		session = models.getSession()

		abtests = session.query(models.ABTest).join(models.Application).filter(models.Application.key == application_key).order_by(models.ABTest.id.desc()).limit(1).all()
		
		if len(abtests) == 1:
			return abtests[0]

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

			return newABTest 

	def getMetrics(self, application_key):
		session = models.getSession()
		return session.query(models.Metrics).join(models.Application).filter(models.Application.key == application_key).first()

	def setMetrics(self, application_key, json):
		session = models.getSession()

		metrics = session.query(models.Metrics).join(models.Application).filter(models.Application.key == application_key).first()
		if metrics:
			models.updateObjectWithJSON(metrics, json, ['key'])
			session.commit()
		return metrics 

	def getPrices(self, application_key):
		session = models.getSession()
		return session.query(models.Prices).join(models.Application).filter(models.Application.key == application_key).all()

	def getPrice(self, prices_key):
		session = models.getSession()
		return session.query(models.Prices).filter_by(key = prices_key).first()

	def getPricingEngine(self, application_key):
		return pricing.PricingEngine(application_key)


	def deletePrices(self, prices_key):
		session = models.getSession()

		# Check if prices is currently used
		# count =  session.query(models.ABTest).join(models.Application).filter(models.Application.key == models.ABTest.application_key).filter(models.ABTest.groupAPrices_key == prices_key).count()
		# if count != 0:
		# 	return 0
		# count =  session.query(models.ABTest).join(models.Application).filter(models.Application.key == models.ABTest.application_key).filter(models.ABTest.groupBPrices_key == prices_key).count()
		# if count != 0:
		# 	return 0
		
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
		return True

	def addPrices(self, application_key, engine, data, path):
		session = models.getSession()
		prices = models.Prices(application_key = application_key, engine=engine, data=data, path=path)
		pricing.PricingEngine.validate(prices)
		session.add(prices)
		session.commit()
		return prices


	def getApplicationSecret(self, application_key):
		session = models.getSession()
		application = session.query(models.Application).filter_by(key = application_key).first()
	
		if application != None:
			return application.secret
		return None
		

	def __repr__(self):
		return 'Content'