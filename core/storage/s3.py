import boto.s3 as s3

from core.storage.storage import Storage

class S3(Storage):

	def __init__(self, settings):
		self.conn = s3.connect_to_region('us-east-1', aws_access_key_id=settings['key'], aws_secret_access_key=settings['secret'])
		self.bucket = self.conn.get_bucket(settings['bucket'])

	def save(self, filename, data):
		k = s3.key.Key(self.bucket)
		k.key = filename
		k.set_contents_from_string(data)

	def count(self):
		return len(list(self.bucket.list()))

	def getFiles(self):
		return self.bucket.list()

	def load(self, filename):
		return self.bucket.get_key(filename).get_contents_as_string()

	def delete(self, filename):
		self.bucket.get_key(filename).delete()
