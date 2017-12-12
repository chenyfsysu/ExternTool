# -*- coding: utf-8 -*-

from Connection improt JsonConnection

class RemoteServer(JsonConnection):
	def __init__(self, ip, port):
		super(RemoteServer, self).__init__(ip, port)

	def bind(self):
		pass

	def connect(self):
		pass

	def listen(self):
		pass