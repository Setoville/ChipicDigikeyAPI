from flask import Flask
from flask import abort
from flask_cors import CORS
import http.client
import json
import config
app = Flask(__name__)
CORS(app)
conn = http.client.HTTPSConnection("api.digikey.com")

acceptableCategories = ["2","21","39"]

@app.route('/')
def hello_world():
	return 'Insert model number as query!'

@app.route('/<model>',methods=['GET'])
def get_things(model):
	total = 0
	while True:
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
		print("RESPONSE!!" + data)

		#category is an INT
		try:
			category = json.loads(data)['Parts'][0]['Category']['Id']
		except Exception:
			print("Exception loading category")
			abort(404)

		#break if the category in the JSON is in the list of acceptable categories
		if category in acceptableCategories:
			#print("found")
			break
		if total > 5:
			abort(404)
		total+=1


	#jsonDataAsList is a JSON
	jsonDataAsList = json.loads(data)

	#jsonDataAsJson['Parts'] is a LIST of size ONE, 
	# Z[0] makes it a DICT

	jsonDataAsDict = jsonDataAsList['Parts'][0]


	#Return value
	returnDict = {}

	# jsonDataAsJson[''] gets the VALUE to the KEY
	try:
		#primaryDatasheet = jsonDataAsDict['PrimaryDatasheet']
		
		returnDict.update({'primaryDatasheet':jsonDataAsDict['PrimaryDatasheet']})

		returnDict.update({'productDescription':jsonDataAsDict['ProductDescription']})
		returnDict.update({'familyText':jsonDataAsDict['Family']['Text']})
		#familyText = jsonDataAsDict['Family']['Text']
		returnDict.update({'digikeyPartNumber':jsonDataAsDict['DigiKeyPartNumber']})
		returnDict.update({'categoryText':jsonDataAsDict['Category']['Text']})
		#categoryText = jsonDataAsDict['Category']['Text']
		returnDict.update({'primaryPhoto':jsonDataAsDict['PrimaryPhoto']})
		#primaryPhoto = jsonDataAsDict['PrimaryPhoto']
		returnDict.update({'manufacturerName':jsonDataAsDict['ManufacturerName']['Text']})
	#	print(primaryPhoto)

		jsonDataAsString = json.dumps(returnDict)

		return jsonDataAsString

	except Exception:
		abort(404)


	abort(404)
	return 0


