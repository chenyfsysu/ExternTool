from singleton import Singleton
from six import add_metaclass


@add_metaclass(Singleton)
class GlobalDispatcher(object):
	def __init__(self):
		pass

	def register(self):
		pass

	def unregister(self):
		pass

	def dispatch(self):
		pass
