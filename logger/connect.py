import telnetlib
import logging


logger = logging.getLogger()
logging.basicConfig(
    filename=None,
    format='%(asctime)s |%(levelname)7s |%(name)20s | %(message)s')
logger.setLevel(logging.DEBUG)


import kisresponse



T = telnetlib.Telnet()

T.open(host= "localhost", port=2501)


r = T.read_very_eager()

class KismetConnect(object):
	'''Kismet connection class to communicate with server over telnet'''
	
	def __init__(self, host = 'localhost', port = 2501):
		self._host = host
		self._port = port
		self._connection = telnetlib.Telnet()
	
	def open(self):
		self._connection.open(host=self._host, port = self._port)

	def process_incoming(self):
		r = self._read()
		
	def _read(self):
		'''reads a single line'''
		r = self._connection.read_until('\n')
		return r.strip('\n')


if __name__ == '__main__':
	K = KismetConnect()
	K.open()
