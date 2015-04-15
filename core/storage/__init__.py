from core.storage.filesystem import Filesystem



def getStorage(configuration):
	if configuration['engine'] == 'core.storage.filesystem':
		return Filesystem(configuration['path'])

