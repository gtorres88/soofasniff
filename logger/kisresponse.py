import logging

logger = logging.getLogger()

_response_types = []

def response(cls):
    _response_types.append(cls)
    logger.debug("Adding response type %s" % cls.__name__)
    return cls

def from_raw(raw):
    ret = None
    for restype in _response_types:
        ret = restype.from_raw(raw)
        if (ret is not None):
            return ret


class KismetResponse(object):
    '''Superclass for kismet response'''
    def __init__(self, text):
        self._text = text

    @classmethod
    def from_raw(cls, string):
        if (string.startswith(cls.key)):
            return cls(string)

@response
class AckResponse(KismetResponse):
    '''Ack Response Type: *ACK ID'''
    key = '*ACK'


@response
class IntroResponse(KismetResponse):
    '''Kismet Intro Response: *KISMET ETC'''

    key = '*KISMET'

@response
class ErrorResponse(KismetResponse):
    '''Kismet Error Response: *ERROR'''
    key = '*ERROR'

@response
class TimeResponse(KismetResponse):
    '''Time Response: *TIME'''

    key = '*TIME'

@response
class ProtocolsResponse(KismetResponse):
    '''Time Response: *PROTOCOLS ETC'''

    key = '*PROTOCOLS'

@response
class ClientResponse(KismetResponse):

    key = '*CLIENT'

    def __init__(self, text):
        super(ClientResponse, self).__init__(text)
        #params in a list, strip out prefix
        self.params = self._text.split()[1:]
        for p in list(self.params):
            if p == '':
                self.params.remove(p)

@response
class UnknownResponse(KismetResponse):
    '''Unkown Response, not implemented, should always be last'''

    key = '*'

