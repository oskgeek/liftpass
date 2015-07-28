import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import event
import datetime
import uuid
import functools
import threading

import config
import core.util.debug as debug


threadData = {}

Base = declarative_base()

def generateUUID():
	return uuid.uuid4().hex.replace('-', '')

if 'sqlite' in config.ContentDatabase['address']:
	engine = sqlalchemy.create_engine(config.ContentDatabase['address'], echo=config.ContentDatabase['debug'], connect_args={'check_same_thread':False})
	event.listen(engine, 'connect', lambda conn, record: conn.execute('pragma foreign_keys=ON'))
else:
	engine = sqlalchemy.create_engine(config.ContentDatabase['address'], echo=config.ContentDatabase['debug'], isolation_level="READ COMMITTED",  pool_size=20, max_overflow=0)

sessionMaker = sessionmaker(bind=engine, autoflush=True)
scopedSessions = scoped_session(sessionMaker)	

def getEngine():
	global engine
	return engine

def getSession():
	global scopedSessions
	return scopedSessions()

def updateObjectWithJSON(object, json, ignore = []):
	for key, val in json.items():
		
		if key in ignore:
			continue

		# Skip if it begins with liftpass-
		if key.find('liftpass-') == 0:
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

	key = Column(String(32), default=generateUUID, primary_key=True)
	secret = Column(String(32), default=generateUUID)

	name = Column(String(32))

	created = Column(DateTime, default=datetime.datetime.utcnow)



class Currencies(Base, CoreBase):
	__tablename__ = 'currencies'

	id = Column(Integer, primary_key=True)

	application_key = Column(String(32), ForeignKey('application.key', ondelete='CASCADE'))
	application = relationship('Application', backref=backref('currencies'))

	currency1 = Column(String(128), nullable=True)
	currency2 = Column(String(128), nullable=True)
	currency3 = Column(String(128), nullable=True)
	currency4 = Column(String(128), nullable=True)
	currency5 = Column(String(128), nullable=True)
	currency6 = Column(String(128), nullable=True)
	currency7 = Column(String(128), nullable=True)
	currency8 = Column(String(128), nullable=True)

	created = Column(DateTime, default=datetime.datetime.utcnow)

class Good(Base, CoreBase):
	__tablename__ = 'goods'

	key = Column(String(32), default=generateUUID, primary_key=True)

	application_key = Column(String(32), ForeignKey('application.key', ondelete='CASCADE'))
	application = relationship('Application', backref=backref('goods'))

	name = Column(String(128))

	created = Column(DateTime, default=datetime.datetime.utcnow)


class Metrics(Base, CoreBase):

	__tablename__ = 'metrics'

	id = Column(Integer, primary_key=True)

	application_key = Column(String(32), ForeignKey('application.key', ondelete='CASCADE'))
	application = relationship('Application', backref=backref('metrics'))

	metricString1 = Column(String(128), nullable=True)
	metricString2 = Column(String(128), nullable=True)
	metricString3 = Column(String(128), nullable=True)
	metricString4 = Column(String(128), nullable=True)
	metricString5 = Column(String(128), nullable=True)
	metricString6 = Column(String(128), nullable=True)
	metricString7 = Column(String(128), nullable=True)
	metricString8 = Column(String(128), nullable=True)

	metricNumber1 = Column(String(128), nullable=True)
	metricNumber2 = Column(String(128), nullable=True)
	metricNumber3 = Column(String(128), nullable=True)
	metricNumber4 = Column(String(128), nullable=True)
	metricNumber5 = Column(String(128), nullable=True)
	metricNumber6 = Column(String(128), nullable=True)
	metricNumber7 = Column(String(128), nullable=True)
	metricNumber8 = Column(String(128), nullable=True)
	metricNumber9 = Column(String(128), nullable=True)
	metricNumber10 = Column(String(128), nullable=True)
	metricNumber11 = Column(String(128), nullable=True)
	metricNumber12 = Column(String(128), nullable=True)
	metricNumber13 = Column(String(128), nullable=True)
	metricNumber14 = Column(String(128), nullable=True)
	metricNumber15 = Column(String(128), nullable=True)
	metricNumber16 = Column(String(128), nullable=True)
	metricNumber17 = Column(String(128), nullable=True)
	metricNumber18 = Column(String(128), nullable=True)
	metricNumber19 = Column(String(128), nullable=True)
	metricNumber20 = Column(String(128), nullable=True)
	metricNumber21 = Column(String(128), nullable=True)
	metricNumber22 = Column(String(128), nullable=True)
	metricNumber23 = Column(String(128), nullable=True)
	metricNumber24 = Column(String(128), nullable=True)

class Prices(Base, CoreBase):

	__tablename__ = 'prices'

	application_key = Column(String(32), ForeignKey('application.key', ondelete='CASCADE'))
	application = relationship('Application', backref=backref('prices'))

	key = Column(String(32), default=generateUUID, primary_key=True)

	data = Column(Text, nullable=True)
	path = Column(String(256), nullable=True)

	engine = Column(String(32))

	deleted = Column(Boolean, default=lambda: False)

	created = Column(DateTime, default=datetime.datetime.utcnow)

class ABTest(Base, CoreBase):

	__tablename__ = 'abtest'	

	id = Column(Integer, primary_key=True)

	application_key = Column(String(32), ForeignKey('application.key', ondelete='CASCADE'))
	application = relationship('Application', backref=backref('abtest'))


	countryWhiteList = Column(String(256), default=str)
	countryBlackList = Column(String(256), default=str)

	modulus = Column(Integer, default=lambda: 2)
	modulusLimit = Column(Integer, default=lambda: 0)

	groupAPrices_key = Column(String(32), ForeignKey('prices.key'), nullable=True)
	groupBPrices_key = Column(String(32), ForeignKey('prices.key'), nullable=True)

	created = Column(DateTime, default=datetime.datetime.utcnow)


class Events(Base, CoreBase):

	__tablename__ = 'events'

	id = Column(Integer, primary_key=True)

	# Application the event belongs to
	application_key = Column(String(32), ForeignKey('application.key', ondelete='CASCADE'))
	application = relationship('Application', backref=backref('events'))

	# The user ID
	user = Column(String(32))

	# User IP address 
	ip = Column(String(32))

	# User country derived from IP address
	country = Column(String(32))

	# Metrics
	metricString1 = Column(String(128), nullable=True)
	metricString2 = Column(String(128), nullable=True)
	metricString3 = Column(String(128), nullable=True)
	metricString4 = Column(String(128), nullable=True)
	metricString5 = Column(String(128), nullable=True)
	metricString6 = Column(String(128), nullable=True)
	metricString7 = Column(String(128), nullable=True)
	metricString8 = Column(String(128), nullable=True)

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
	name = Column(String(128))

	# Event attributes
	attributeString1 = Column(String(128), nullable=True)
	attributeString2 = Column(String(128), nullable=True)
	attributeString3 = Column(String(128), nullable=True)
	attributeString4 = Column(String(128), nullable=True)
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



def create():
	Application.__table__.create(getEngine(), checkfirst=True)
	Currencies.__table__.create(getEngine(), checkfirst=True)
	Good.__table__.create(getEngine(), checkfirst=True)
	Metrics.__table__.create(getEngine(), checkfirst=True)
	Prices.__table__.create(getEngine(), checkfirst=True)
	ABTest.__table__.create(getEngine(), checkfirst=True)
	Events.__table__.create(getEngine(), checkfirst=True)

def flush():
	

	# s = getSession()
	for table in [Application, Currencies, Good, Metrics, ABTest, Prices, Events]:
		try:
			# rows = s.query(table).count()
			rows = 0
			debug.log('Deleting table %s with %d rows'%(table.__name__, rows))
			table.__table__.drop(getEngine())
			# s.commit()
			# s.flush()
		except Exception as e:
			debug.error('%s'%e)
	

def execute(sql):

	session = getSession()
	session.execute(sql)
	session.close()