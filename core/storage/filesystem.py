import uuid
import os

from core.storage.storage import Storage
import config


class Filesystem(Storage):

	def __init__(self, root):
		self.root = root
		pass

	def save(self, filename, data):
		f = open('%s/%s'%(self.root, filename), 'w+')
		f.write(data)
		f.close()

	def saveStream(self, filename):
		return open('%s/%s'%(self.root, filename), 'w+')

	def count(self):
		return len(os.listdir(self.root))

	def getFiles(self):
		return os.listdir(self.root)

	def load(self, filename):
		f = open('%s/%s'%(self.root, filename), 'r')
		return f.read()

