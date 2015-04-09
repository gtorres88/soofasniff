import telnetlib
import logging


logger = logging.getLogger()
logging.basicConfig(
    filename=None,
    format='%(asctime)s |%(levelname)7s |%(name)20s | %(message)s')
logger.setLevel(logging.DEBUG)


from kisresponse import *

class KismetConnect(object):
    '''Kismet connection class to communicate with server over telnet'''
    
    def __init__(self, host = 'localhost', port = 2501):
        self._host = host
        self._port = port
        self._connection = telnetlib.Telnet()
    
    def open(self):
        self._connection.open(host=self._host, port = self._port)
        self._wait_for_intro()

    def process_incoming(self):
        r = self._read()
        resp = from_raw(r)
        if (resp is not None):
            logger.debug("Received raw response: %s, of type: %s" % (r, resp))
            return resp

    def _wait_for_intro(self):

        logger.info("Waiting for intro messages from kismet. If these do not \
arrive, Kismet server may not be running")
        r = self.process_incoming()
        while(isinstance(r, IntroResponse) is False):
            r = self.process_incoming()
        while(isinstance(r, ProtocolsResponse) is False):
            r = self.process_incoming()
        logger.info("Intro message received")
        

    def _read(self):
        '''reads a single line'''
        r = self._connection.read_until('\n')
        return r.strip('\n')


if __name__ == '__main__':
    K = KismetConnect()
    K.open()

    try:
        while(1):
            K.process_incoming()
    except KeyboardInterrupt:
        logger.info("Crtl-C caught. Exiting")

