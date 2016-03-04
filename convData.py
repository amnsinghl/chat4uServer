class ConvData(object):
	gcmToken = ""
	requestId = 0
	serviceId = 0
	assignedPerson = ""

	def __init__(self, gcmToken ,requestId ,serviceId ):
		self.gcmToken = gcmToken
		self.requestId = requestId
		self.serviceId = serviceId
