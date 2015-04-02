
class Cache:

	def __init__(self, function):
		self.function = function
		self.value = None

	def __call__(self):
		if self.value == None:
			self.value = self.function()
		return self.value


class Memoize(dict):

	def __init__(self, function):

		self.function = function

	def __call__(self, *args):
		if args not in self:
			self[args] = self.function(args)
		return self[args]
