
class DataEngineException(Exception):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message

class ApplicationNotFoundException(Exception):
	def __str__(self):
		return 'No application found given the application key'

class NoPricingForGroup(Exception):
	def __str__(self):
		return 'Application has no defined prices for group'
