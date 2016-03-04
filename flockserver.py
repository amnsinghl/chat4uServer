from flask import Flask, request
import json
import urllib2
from random import randint
from convData import ConvData
from flockPerson import FlockPerson

app = Flask(__name__)

tokenToConvData = {}
requestIdToConvData = {}
serviceMap = {}
availMap = {}
@app.route('/startConversation',methods=['POST'])
def startConversation():
	data = json.loads(request.data)
	print data
	gcmToken = data['gcmToken']
	serviceId = data['serviceId']
	requestId = str(randint(0,999999))
	convData =  ConvData(gcmToken, requestId, serviceId)
	ret = ""
	if assignPerson(convData):
		ret = "{\"requestId\":" + requestId + "}"
	else:
		ret = "{\"could not assign a person\"}"
	print ret
	return ret


def assignPerson(convData):
	dataList = serviceMap[str(convData.serviceId)]
	for data in dataList:
		if availMap[data.flockToken]:
			availMap[data.flockToken] = False
			print "token: " + data.flockToken + " assigned to" + convData.requestId
			convData.assignedPerson = data
			tokenToConvData[data.flockToken] = convData
			requestIdToConvData[convData.requestId] = convData
			print requestIdToConvData
			return True
	return False

def endConversation(convData):
	availMap[convData.assignedPerson.flockToken] = True
	requestIdToConvData.pop(convData.requestId, None)
	tokenToConvData.pop(convData.assignedPerson.flockToken, None)


@app.route('/getServices',methods=['GET'])
def getServices():
	with open('services.json', 'r') as myfile:
		services = myfile.read()
		return services

@app.route('/flockToServer',methods=['POST'])
def flockToUs():
	data = json.loads(request.data)
	print data
	token = request.args.get('token')
	text = data['text']
	if text.startswith("#register"):
		arr = text.split()
		createNewFlockPerson(arr[1], token, arr[2])
		return "OK"

	convData = tokenToConvData[token]
	if text.startswith("#stop"):
		sendToGcm("Chat Ended", convData)
		endConversation(convData)
	else:
		sendToGcm(text, convData)

	return "OK"

@app.route('/appToServer',methods=['POST'])
def appToUs():
	data = json.loads(request.data)
	print data
	text = data['text']
	requestId = data['requestId']
	convData = requestIdToConvData[requestId]
	print convData
	sendToFlock(text, convData)
	return "OK"

@app.route('/endChat',methods=['POST'])
def endChat():
	data = json.loads(request.data)
	print data
	requestId = data['requestId']
	convData = requestIdToConvData[requestId]
	endConversation(convData)
	return "OK"

def sendToFlock(message, convData):
	data = {
		"text": message
	}

	req = urllib2.Request(convData.assignedPerson.webhookUrl)
	req.add_header('Content-Type', 'application/json')
	response = urllib2.urlopen(req, json.dumps(data))

def sendToGcm(message, convData):
	data = {
		"message": message,
		"requestId": convData.requestId,
		"registrationId": convData.gcmToken
	}

	req = urllib2.Request("http://www.dhiwal.com:9003/sendMessage")   #gcm server url
	req.add_header('Content-Type', 'application/json')
	response = urllib2.urlopen(req, json.dumps(data))

def createNewFlockPerson(serviceId, token, webhookUrl):
	flockPerson = FlockPerson(token, webhookUrl)
	serviceId = str(serviceId)
	print flockPerson
	if not serviceId in serviceMap:
		serviceMap[serviceId] = []
	serviceMap[serviceId].append(flockPerson)
	availMap[token] = True
	print str(availMap)
	print str(serviceMap)

def populateMaps():
	lis = ["a", "b", "c" ,"d"]
	serviceMap["1"] = []
	for l in lis:
		availMap[l] = True
		serviceMap["1"].append(FlockPerson(l, "http://localhost:8081"))

	lis = ["e", "f", "g" ,"h"]
	serviceMap["2"] = []
	for l in lis:
		availMap[l] = True
		serviceMap["2"].append(FlockPerson(l, "http://localhost:8081"))
	print str(availMap)
	print str(serviceMap)

if __name__ == '__main__':
	populateMaps()
	app.run(host= '0.0.0.0', port=8080)
















