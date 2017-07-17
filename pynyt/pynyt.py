import requests
import json

# Get headlines for first 10 articles
def query(params, api_key):
    url = "http://api.nytimes.com/svc/search/v2/articlesearch.json"
    r = requests.get(url, headers={'api-key': key}, params=params)
    parsed_json = json.loads(r.text)

    headlines = []
    for article in parsed_json['response']['docs']:
        headlines.append(article['headline']['main'])