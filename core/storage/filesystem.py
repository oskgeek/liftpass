import uuid
import os

from core.storage.storage import Storage
import config


class Filesystem(Storage):

	def __init__(self):
		pass

	def save(self, filename, data):
		f = open('%s/%s'%(config.StoragePath, filename), 'w+')
		f.write(data)
		f.close()

	def count(self):
		return len(os.listdir(config.StoragePath))