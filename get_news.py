import requests
import json

subscription_key = "ce49e11f62904abe80742c3c2de79891"
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news?mkt=en-us"
headers = {"Ocp-Apim-Subscription-Key" : subscription_key}

def headline():
	response = requests.get(search_url, headers=headers)
	response.raise_for_status()
	search_results = json.dumps(response.json(), ensure_ascii=False)
	search_results = json.loads(search_results)

	return search_results

test = headline()