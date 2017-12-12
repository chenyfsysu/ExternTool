# import sys
# from core.GlobalDispatcher import GlobalDispatcher

# if __name__ == '__main__':
#    print GlobalDispatcher()
#    print GlobalDispatcher()

import json
import socket
import struct
import logging
import time

logger = logging.getLogger("jsocket")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


			
	timeout = property(_get_timeout, _set_timeout,doc='Get/set the socket timeout')
	address = property(_get_address, _set_address,doc='read only property socket address')
	port = property(_get_port, _set_port,doc='read only property socket port')

	
class JsonServer(JsonSocket):
	def __init__(self, address='127.0.0.1', port=5489):
		super(JsonServer, self).__init__(address, port)
		self._bind()
	
	def _bind(self):
		self.socket.bind( (self.address,self.port) )

	def _listen(self):
		self.socket.listen(1)
	
	def _accept(self):
		return self.socket.accept()
	
	def accept_connection(self):
		self._listen()
		self.conn, addr = self._accept()
		self.conn.settimeout(self.timeout)
		logger.debug("connection accepted, conn socket (%s,%d)" % (addr[0],addr[1]))
	
	def _is_connected(self):
		return True if not self.conn else False
	
	connected = property(_is_connected, doc="True if server is connected")

	
class JsonClient(JsonSocket):
	def __init__(self, address='127.0.0.1', port=5489):
		super(JsonClient, self).__init__(address, port)
		
	def connect(self):
		for i in range(10):
			try:
				self.socket.connect( (self.address, self.port) )
			except socket.error as msg:
				logger.error("SockThread Error: %s" % msg)
				time.sleep(3)
				continue
			logger.info("...Socket Connected")
			return True
		return False

	
if __name__ == "__main__":
	""" basic json echo server """
	import threading
	
	def server_thread():
		logger.debug("starting JsonServer")
		server = JsonServer()
		server.accept_connection()
		while 1:
			try:
				msg = server.read_obj()
				logger.info("server received: %s" % msg)
				server.send_obj(msg)
			except socket.timeout as e:
				logger.debug("server socket.timeout: %s" % e)
				continue
			except Exception as e:
				logger.error("server: %s" % e)
				break
			
		server.close()
			
	t = threading.Timer(1,server_thread)
	t.start()
	
	time.sleep(2)
	logger.debug("starting JsonClient")
	
	client = JsonClient()
	client.connect()
		
	i = 0
	while i < 10:
		client.send_obj({"i": i})
		try:
			msg = client.read_obj()
			logger.info("client received: %s" % msg)
		except socket.timeout as e:
			logger.debug("client socket.timeout: %s" % e)
			continue
		except Exception as e:
			logger.error("client: %s" % e)
			break
		i = i + 1
	
	client.close()
