import config
import importlib
from util.memoize import Memoize, Cache


def importEngine(name):
	moduleName = name[0:name.rfind('.')]
	className = name[name.rfind('.')+1:]
	m = importlib.import_module(moduleName)
	return getattr(m, className)

@Cache
def getAnalytics():
	return importEngine(config.AnalyticsEngine)()

@Cache
def getContent():
	from engine.content import Content
	return Content()

@Cache
def getMonitor():
	return importEngine(config.MonitorEngine)()

@Cache
def getStorage():
	return importEngine(config.StorageEngine)()
