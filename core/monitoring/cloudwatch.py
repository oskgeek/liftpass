from boto.ec2.cloudwatch import CloudWatchConnection
import boto.utils 
import time

from core.monitoring.base import Monitor


class CloudWatchTimer:

	def __init__(self, cloudwatch, metric):
		self.metric = metric
		self.cloudwatch = cloudwatch

	def __enter__(self):
		self.start = time.time()

	def __exit__(self, type, value, traceback):
		self.cloudwatch.put(self.metric, time.time()-self.start, 'Milliseconds')



class CloudWatch(Monitor):

	def __init__(self, settings):
		self.conn = CloudWatchConnection(settings['key'], settings['secret'])
		self.namespace = settings['namespace']


	def put(self, metric, value, unit):
		instance = boto.utils.get_instance_metadata()['instance-id']		
		self.conn.put_metric_data(self.namespace, name=metric, value=value, unit=unit, dimensions={'instance-id':instance})

	def count(self, metric):
		self.put(metric, 1, 'Count')

	def time(self, metric):
		return CloudWatchTimer(self, metric)
