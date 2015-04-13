# import core.storage.storage as storage
from core.storage.filesystem import Filesystem
import config

def getDefaultStorage():
	if config.StorageEngine == 'core.storage.filesystem':
		return Filesystem()