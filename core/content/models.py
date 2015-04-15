import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session
import datetime
import uuid
import functools

import config

engine = sqlalchemy.create_engine(config.ContentAddress, echo=config.ContentDebug)
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

	currencies = relationship('Currencies', backref='application')
	goods = relationship('Good')
	metrics = relationship('Metrics', backref='application')
	prices = relationship('Prices', backref='application')
	abtest = relationship('ABTest', backref='application')

	created = Column(DateTime, default=datetime.datetime.utcnow)



class Currencies(Base, CoreBase):
	__tablename__ = 'currencies'

	id = Column(Integer, primary_key=True)

	application_key = Column(Integer, ForeignKey('application.key', ondelete='CASCADE'))
	

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

	name = Column(String)

	created = Column(DateTime, default=datetime.datetime.utcnow)


class Metrics(Base, CoreBase):

	__tablename__ = 'metrics'

	id = Column(Integer, primary_key=True)

	application_key = Column(Integer, ForeignKey('application.key', ondelete='CASCADE'))

	str1 = Column(String, nullable=True)
	str2 = Column(String, nullable=True)
	str3 = Column(String, nullable=True)
	str4 = Column(String, nullable=True)
	str5 = Column(String, nullable=True)
	str6 = Column(String, nullable=True)
	str7 = Column(String, nullable=True)
	str8 = Column(String, nullable=True)

	num1 = Column(String, nullable=True)
	num2 = Column(String, nullable=True)
	num3 = Column(String, nullable=True)
	num4 = Column(String, nullable=True)
	num5 = Column(String, nullable=True)
	num6 = Column(String, nullable=True)
	num7 = Column(String, nullable=True)
	num8 = Column(String, nullable=True)
	num9 = Column(String, nullable=True)
	num10 = Column(String, nullable=True)
	num11 = Column(String, nullable=True)
	num12 = Column(String, nullable=True)
	num13 = Column(String, nullable=True)
	num14 = Column(String, nullable=True)
	num15 = Column(String, nullable=True)
	num16 = Column(String, nullable=True)
	num17 = Column(String, nullable=True)
	num18 = Column(String, nullable=True)
	num19 = Column(String, nullable=True)
	num20 = Column(String, nullable=True)
	num21 = Column(String, nullable=True)
	num22 = Column(String, nullable=True)
	num23 = Column(String, nullable=True)
	num24 = Column(String, nullable=True)

class ABTest(Base, CoreBase):

	__tablename__ = 'abtest'	

	id = Column(Integer, primary_key=True)

	application_key = Column(Integer, ForeignKey('application.key', ondelete='CASCADE'))

	countryWhiteList = Column(String, default=str)
	countryBlackList = Column(String, default=str)

	modulus = Column(Integer, default=lambda: 2)
	modulusLimit = Column(Integer, default=lambda: 0)

	dynamicPrices_key = Column(String, ForeignKey('prices.key', ondelete='CASCADE'), nullable=True)
	staticPrices_key = Column(String, ForeignKey('prices.key', ondelete='CASCADE'), nullable=True)


class Prices(Base, CoreBase):

	__tablename__ = 'prices'

	application_key = Column(Integer, ForeignKey('application.key', ondelete='CASCADE'))

	key = Column(String, default=generateUUID, primary_key=True)

	data = Column(Text, nullable=True)
	path = Column(String, nullable=True)

	engine = Column(String)

	created = Column(DateTime, default=datetime.datetime.utcnow)


Application.__table__.create(engine, checkfirst=True)
Currencies.__table__.create(engine, checkfirst=True)
Good.__table__.create(engine, checkfirst=True)
Metrics.__table__.create(engine, checkfirst=True)
ABTest.__table__.create(engine, checkfirst=True)
Prices.__table__.create(engine, checkfirst=True)


