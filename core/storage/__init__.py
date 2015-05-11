from core.storage.filesystem import Filesystem
from core.storage.s3 import S3


def getStorage(configuration):
	if configuration['engine'] == 'core.storage.filesystem':
		return Filesystem(configuration['path'])
	elif configuration['engine'] == 'core.storage.s3':
		return S3(configuration)
