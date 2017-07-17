import requests
import json
import sys

class NYTArticleAPIObject:
    def __init__(self, api_key):
        self.url = "http://api.nytimes.com/svc/search/v2/articlesearch.json"
        self.api_key = api_key

    def check_params(self, params):
        valid_params = ['q', 'fq', 'begin_date', 'end_date', 'sort', 'fl', 'hl', 'page',
                        'facet_field', 'facet_filter']
                        
        for param in params:
            try:
                valid_params.index(param)
            except ValueError:
                print("Invalid query parameter: ", param)

    # Get headlines for first 10 articles
    def query(self, params={}, all_pages=False):
        r = requests.get(self.url, headers={'api-key': self.api_key}, params=params)
        parsed_json = json.loads(r.text)

        self.check_params(params)

        headlines = []
        for article in parsed_json['response']['docs']:
            headlines.append(article['headline']['main'])

        return headlines