from flask import Flask
import http.client
import config
app = Flask(__name__)
conn = http.client.HTTPSConnection("api.digikey.com")
@app.route('/')
def hello_world():
	return 'Insert model number as query!'

@app.route('/<model>',methods=['GET'])
def get_things(model):

	payload = "{\"SearchOptions\":[\"CollapsePackingTypes\"],\"Keywords\":\"p5555-nd\",\"RecordCount\":\"10\",\"RecordStartPosition\":\"0\",\"Filters\":{\"CategoryIds\":[57203494],\"FamilyIds\":[69149394],\"ManufacturerIds\":[44865313],\"ParametricFilters\":[{\"ParameterId\":\"725\",\"ValueId\":\"7\"}]},\"Sort\":{\"Option\":\"SortByUnitPrice\",\"Direction\":\"Ascending\",\"SortParameterId\":\"50\"},\"RequestedQuantity\":\"50\"}"
	client_id = config.HT6_CLIENT_ID
	access_token = config.HT6_ACCESS_TOKEN
	headers = {
		'x-ibm-client-id': client_id,
		'x-digikey-locale-site': "CA",
		'x-digikey-locale-language': "en",
		'x-digikey-locale-currency': "CAD",
		'authorization': access_token,
		'content-type': "application/json",
		'accept': "application/json"
		}

	conn.request("POST", "/services/partsearch/v2/keywordsearch", payload, headers)

	res = conn.getresponse()
	data = res.read()

	print(data.decode("utf-8"))
	return data.decode("utf-8")