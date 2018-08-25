from flask import Flask
import http.client
import json
import config
app = Flask(__name__)
conn = http.client.HTTPSConnection("api.digikey.com")
@app.route('/')
def hello_world():
	return 'Insert model number as query!'

@app.route('/<model>',methods=['GET'])
def get_things(model):

	payloadFirstHalf = "{\"SearchOptions\":[\"CollapsePackingTypes\"],\"Keywords\":\""
	payloadSecondHalf = "\",\"RecordCount\":\"1\",\"RecordStartPosition\":\"0\",\"Sort\":{\"Option\":\"SortByUnitPrice\",\"Direction\":\"Ascending\",\"SortParameterId\":\"50\"},\"RequestedQuantity\":\"50\"}"
	payload = payloadFirstHalf+model+payloadSecondHalf
	clientID = config.HT6_CLIENT_ID
	accessToken = config.HT6_ACCESS_TOKEN
	headers = {
		'x-ibm-client-id': clientID,
		'x-digikey-locale-site': "CA",
		'x-digikey-locale-language': "en",
		'x-digikey-locale-currency': "CAD",
		'authorization': accessToken,
		'content-type': "application/json",
		'accept': "application/json"
		}

	conn.request("POST", "/services/partsearch/v2/keywordsearch", payload, headers)

	res = conn.getresponse()
	rawData = res.read()
	data = rawData.decode("utf-8")
	json.dumps(data)
	jsonData = json.loads(data)
	jsonData[0]
	return 