import telnetlib
import logging
from kisresponse import *

logger = logging.getLogger()

class KismetConnect(object):
    '''Kismet connection class to communicate with server over telnet'''
    
    def __init__(self, host = 'localhost', port = 2501):
        self._host = host
        self._port = port
        self._connection = telnetlib.Telnet()
        self._opened = False

    
    def open(self):
        '''Opens connection to kismet server'''
        self._connection.open(host=self._host, port = self._port)
        self._opened = True
        self._wait_for_intro()
        self._count = 0

    def close(self):
        '''close connection'''
        if (self._opened):
            self._connection.close()
            self._opened = False

    def process_incoming(self):
        '''Processes and returns messages in object format'''
        if (self._opened is False):
            logger.error("Connection has not been opened")
            raise Exception

        r = self._read()
        resp = from_raw(r)
        if (resp is not None):
            logger.debug("Received raw response: %s, of type: %s" % (r, resp))
            return resp

    def send_cmd(self, cmd, args = None):
        '''sends a single command with arguments

        Note: args functionality not yet implemented'''

        cmdstring = "!%d %s" % (self._count, cmd)
        logger.debug("Sending Command: %s" % cmdstring)
        self._connection.write(cmdstring + "\n")
        self._count =+ 1

    def _wait_for_intro(self):
        '''waits for the kismet intro messages'''
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



