import uuid
import os

from core.storage.storage import Storage
import config


class Filesystem(Storage):

	def __init__(self, root):
		self.root = root
		pass

	def save(self, filename, data):
		f = open(os.path.join(self.root, filename), 'w+')
		f.write(data)
		f.close()

	def count(self):
		return len(os.listdir(self.root))

	def getFiles(self):
		return os.listdir(self.root)

	def load(self, filename):
		f = open(os.path.join(self.root, filename), 'r')
		return f.read()

	def delete(self, filename):
		os.remove(os.path.join(self.root, filename))
