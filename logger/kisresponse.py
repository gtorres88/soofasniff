import logging

logger = logging.getLogger()

_response_types = []



def response(cls):
	_response_types.append(cls)
	logger.debug("Adding response type %s" % cls.__name__)

def from_raw(raw):
    ret = None
    for restype in _response_types:
        ret = restype.from_raw(raw)
        if (ret is not None):
            return ret

@response
class AckResponse(object):
	'''Ack Response Type: *ACK ID'''

    key = '*ACK'

	def __init__(self, text):
        self._text = text


	@classmethod
	def from_raw(cls, string):
        if (string.startswith(cls.key)):
            return cls.__init__(string)

@response
class IntroResponse(object):
	'''Kismet Intro Response: *KISMET ETC'''

    key = '*KISMET'

	def __init__(self, text):
        self._text = text

	@classmethod
	def from_raw(cls, string):
        return None

@response
class ErrorResponse(object):

    key = '*ERROR'

	'''Kismet Error Response: *ERROR'''
	def __init__(self):
		pass

@response
class TimeResponse(object):
	'''Time Response: *TIME'''

    key = '*TIME'

	def __init__(self):
		pass


@response
class ProtocolsResponse(object):
	'''Time Response: *PROTOCOLS ETC'''

    key = '*PROTOCOLS'

	def __init__(self):
		pass
@response
class UnknownResponse(object):

	'''Unkown Response, not implemented, should always be last'''

    key = '*'

	def __init__(self):
		pass



