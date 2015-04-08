import logging

logger = logging.getLogger()

_response_types = []


class KismetResponse(object):
	'''Kismet response class'''

	def __init__(self, string):
		pass



def response(cls):
	_response_types.append(cls)
	logger.debug("Adding response type %s" % cls.__name__)

def from_raw(raw):
	pass


@response
class AckResponse(KismetResponse):
	'''Ack Response Type: *ACK ID'''

	@classmethod
	def from_raw(cls, string):
		#check if ACK

@response
class IntroResponse(KismetResponse):
	'''Kismet Intro Response: *KISMET ETC'''

	def __init__(self):
		pass

@response
class ErrorResponse(KismetResponse):
	'''Kismet Error Response: *ERROR'''
	def __init__(self):
		pass

@response
class TimeResponse(KismetResponse):
	'''Time Response: *TIME'''

	def __init__(self):
		pass


@response
class ProtocolsResponse(KismetResponse):
	'''Time Response: *PROTOCOLS ETC'''

	def __init__(self):
		pass
@response
class UnknownResponse(KismetResponse):
	'''Unkown Response, not implemented'''

	def __init__(self):
		pass

