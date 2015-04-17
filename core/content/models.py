import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import event
import datetime
import uuid
import functools

import config

engine = sqlalchemy.create_engine(config.ContentAddress, echo=config.ContentDebug)
event.listen(engine, 'connect', lambda conn, record: conn.execute('pragma foreign_keys=ON'))

Base = declarative_base()
sessions = sessionmaker(bind=engine)
scopedSessions = scoped_session(sessions)

def getSession():
	return scopedSessions()

def generateUUID():
	return uuid.uuid4().hex.replace('-', '')

def updateObjectWithJSON(object, json, ignore = []):
	for key, val in json.items():
		
		if key in ignore:
			continue

		# Skip if it begins with gondola-
		if key.find('gondola-') == 0:
			continue

		# Set attribute if object has it
		if hasattr(object, key):
			setattr(object, key, val)
		else: 
			print('%s model object does not have attribute "%s"'%(type(object).__name__, key))
			# ABTest does not have specified attribute
			pass
	return object


class CoreBase:
	def as_dict(self):
		res = {}
		for c in self.__table__.columns:
			if c.name not in ['id']:
				res[c.name] = getattr(self, c.name)
		return res
		

class Application(Base, CoreBase):
	__tablename__ = 'application'

	key = Column(String, default=generateUUID, primary_key=True)
	secret = Column(String, default=generateUUID)

	name = Column(String)

	created = Column(DateTime, default=datetime.datetime.utcnow)



class Currencies(Base, CoreBase):
	__tablename__ = 'currencies'

	id = Column(Integer, primary_key=True)

	application_key = Column(Integer, ForeignKey('application.key', ondelete='CASCADE'))
	application = relationship('Application', backref=backref('currencies'))

	currency1 = Column(String, nullable=True)
	currency2 = Column(String, nullable=True)
	currency3 = Column(String, nullable=True)
	currency4 = Column(String, nullable=True)
	currency5 = Column(String, nullable=True)
	currency6 = Column(String, nullable=True)
	currency7 = Column(String, nullable=True)
	currency8 = Column(String, nullable=True)

	created = Column(DateTime, default=datetime.datetime.utcnow)

class Good(Base, CoreBase):
	__tablename__ = 'goods'

	key = Column(String, default=generateUUID, primary_key=True)

	application_key = Column(Integer, ForeignKey('application.key', ondelete='CASCADE'))
	application = relationship('Application', backref=backref('goods'))

	name = Column(String)

	created = Column(DateTime, default=datetime.datetime.utcnow)


class Metrics(Base, CoreBase):

	__tablename__ = 'metrics'

	id = Column(Integer, primary_key=True)

	application_key = Column(Integer, ForeignKey('application.key', ondelete='CASCADE'))
	application = relationship('Application', backref=backref('metrics'))

	metricString1 = Column(String, nullable=True)
	metricString2 = Column(String, nullable=True)
	metricString3 = Column(String, nullable=True)
	metricString4 = Column(String, nullable=True)
	metricString5 = Column(String, nullable=True)
	metricString6 = Column(String, nullable=True)
	metricString7 = Column(String, nullable=True)
	metricString8 = Column(String, nullable=True)

	metricNumber1 = Column(String, nullable=True)
	metricNumber2 = Column(String, nullable=True)
	metricNumber3 = Column(String, nullable=True)
	metricNumber4 = Column(String, nullable=True)
	metricNumber5 = Column(String, nullable=True)
	metricNumber6 = Column(String, nullable=True)
	metricNumber7 = Column(String, nullable=True)
	metricNumber8 = Column(String, nullable=True)
	metricNumber9 = Column(String, nullable=True)
	metricNumber10 = Column(String, nullable=True)
	metricNumber11 = Column(String, nullable=True)
	metricNumber12 = Column(String, nullable=True)
	metricNumber13 = Column(String, nullable=True)
	metricNumber14 = Column(String, nullable=True)
	metricNumber15 = Column(String, nullable=True)
	metricNumber16 = Column(String, nullable=True)
	metricNumber17 = Column(String, nullable=True)
	metricNumber18 = Column(String, nullable=True)
	metricNumber19 = Column(String, nullable=True)
	metricNumber20 = Column(String, nullable=True)
	metricNumber21 = Column(String, nullable=True)
	metricNumber22 = Column(String, nullable=True)
	metricNumber23 = Column(String, nullable=True)
	metricNumber24 = Column(String, nullable=True)

class ABTest(Base, CoreBase):

	__tablename__ = 'abtest'	

	id = Column(Integer, primary_key=True)

	application_key = Column(Integer, ForeignKey('application.key', ondelete='CASCADE'))
	application = relationship('Application', backref=backref('abtest'))


	countryWhiteList = Column(String, default=str)
	countryBlackList = Column(String, default=str)

	modulus = Column(Integer, default=lambda: 2)
	modulusLimit = Column(Integer, default=lambda: 0)

	dynamicPrices_key = Column(String, ForeignKey('prices.key'), nullable=True)
	staticPrices_key = Column(String, ForeignKey('prices.key'), nullable=True)


class Prices(Base, CoreBase):

	__tablename__ = 'prices'

	application_key = Column(Integer, ForeignKey('application.key', ondelete='CASCADE'))
	application = relationship('Application', backref=backref('prices'))

	key = Column(String, default=generateUUID, primary_key=True)

	data = Column(Text, nullable=True)
	path = Column(String, nullable=True)

	engine = Column(String)

	created = Column(DateTime, default=datetime.datetime.utcnow)

class Events(Base, CoreBase):

	__tablename__ = 'events'

	id = Column(Integer, primary_key=True)

	# Application the event belongs to
	application_key = Column(Integer, ForeignKey('application.key', ondelete='CASCADE'))
	application = relationship('Application', backref=backref('events'))

	# The user ID
	user = Column(String)

	# User IP address 
	ip = Column(String)

	# User country derived from IP address
	country = Column(String)

	# Metrics
	metricString1 = Column(String, nullable=True)
	metricString2 = Column(String, nullable=True)
	metricString3 = Column(String, nullable=True)
	metricString4 = Column(String, nullable=True)
	metricString5 = Column(String, nullable=True)
	metricString6 = Column(String, nullable=True)
	metricString7 = Column(String, nullable=True)
	metricString8 = Column(String, nullable=True)

	metricNumber1 = Column(Float, nullable=True)
	metricNumber2 = Column(Float, nullable=True)
	metricNumber3 = Column(Float, nullable=True)
	metricNumber4 = Column(Float, nullable=True)
	metricNumber5 = Column(Float, nullable=True)
	metricNumber6 = Column(Float, nullable=True)
	metricNumber7 = Column(Float, nullable=True)
	metricNumber8 = Column(Float, nullable=True)
	metricNumber9 = Column(Float, nullable=True)
	metricNumber10 = Column(Float, nullable=True)
	metricNumber11 = Column(Float, nullable=True)
	metricNumber12 = Column(Float, nullable=True)
	metricNumber13 = Column(Float, nullable=True)
	metricNumber14 = Column(Float, nullable=True)
	metricNumber15 = Column(Float, nullable=True)
	metricNumber16 = Column(Float, nullable=True)
	metricNumber17 = Column(Float, nullable=True)
	metricNumber18 = Column(Float, nullable=True)
	metricNumber19 = Column(Float, nullable=True)
	metricNumber20 = Column(Float, nullable=True)
	metricNumber21 = Column(Float, nullable=True)
	metricNumber22 = Column(Float, nullable=True)
	metricNumber23 = Column(Float, nullable=True)
	metricNumber24 = Column(Float, nullable=True)

	# Name of the event
	name = Column(String)

	# Event attributes
	attributeString1 = Column(String, nullable=True)
	attributeString2 = Column(String, nullable=True)
	attributeString3 = Column(String, nullable=True)
	attributeString4 = Column(String, nullable=True)
	attributeNumber1 = Column(Float, nullable=True)
	attributeNumber2 = Column(Float, nullable=True)
	attributeNumber3 = Column(Float, nullable=True)
	attributeNumber4 = Column(Float, nullable=True)
	attributeNumber5 = Column(Float, nullable=True)
	attributeNumber6 = Column(Float, nullable=True)
	attributeNumber7 = Column(Float, nullable=True)
	attributeNumber8 = Column(Float, nullable=True)
	attributeNumber9 = Column(Float, nullable=True)
	attributeNumber10 = Column(Float, nullable=True)
	attributeNumber11 = Column(Float, nullable=True)
	attributeNumber12 = Column(Float, nullable=True)

	# When the event was triggered in UTC time
	timestamp  = Column(DateTime)

	# When the event was added to database
	created = Column(DateTime, default=datetime.datetime.utcnow)




Application.__table__.create(engine, checkfirst=True)
Currencies.__table__.create(engine, checkfirst=True)
Good.__table__.create(engine, checkfirst=True)
Metrics.__table__.create(engine, checkfirst=True)
ABTest.__table__.create(engine, checkfirst=True)
Prices.__table__.create(engine, checkfirst=True)
Events.__table__.create(engine, checkfirst=True)


