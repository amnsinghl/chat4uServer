class FlockPerson(object):
	flockToken = ""
	webhookUrl = ""
	
	def __init__(self, flockToken ,webhookUrl):
		self.flockToken = flockToken
		self.webhookUrl = webhookUrl

	# def __init__(self, flockToken ):
	# 	self.flockToken = flockToken
	# 	self.webhookUrl = "http://localhost:8081/"

	def __repr__(self):
		return "flockToken: " + self.flockToken + "," + " webhookUrl: " + self.webhookUrl;
