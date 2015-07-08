

class MonitorTimer:

	def __init__(self, monitor, metric):
		pass
	def __enter__(self):
		pass

	def __exit__(self, type, value, traceback):
		pass


class Monitor:

	def __init__(self, settings):
		pass

	def put(self, metric, value, units):
		pass

	def count(self, metric):
		pass

	def time(self, metric):
		return MonitorTimer(self, metric)