import boto.s3 as s3
import threading

from core.storage.storage import Storage

class IterableWrap:

	def __init__(self, data, attribute):
		self.data = data
		self.attribute = attribute

	def __iter__(self):
		return self

	def __next__(self):
		return getattr(self.data.__next__(), self.attribute)



class S3(Storage):

	def __init__(self, settings):
		self.conn = s3.connect_to_region('us-east-1', aws_access_key_id=settings['key'], aws_secret_access_key=settings['secret'])
		self.bucket = self.conn.get_bucket(settings['bucket'])

	def save(self, filename, data):
		t = threading.Thread(target=self.__saveAux, args=(filename, data))
		t.start()

	def __saveAux(self, filename, data):
		k = s3.key.Key(self.bucket)
		k.key = filename
		k.set_contents_from_string(data)

	def count(self):
		return len(list(self.bucket.list()))

	def getFiles(self):
		return IterableWrap(iter(self.bucket.list()), 'name')

	def load(self, filename):
		return self.bucket.get_key(filename).get_contents_as_string().decode('utf-8')

	def delete(self, filename):
		self.bucket.get_key(filename).delete()
