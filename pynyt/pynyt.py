import requests
import json
import sys
import time


class NYTArticleAPIObject:
    def __init__(self, api_key):
        self.url = "http://api.nytimes.com/svc/search/v2/articlesearch.json"
        self.api_key = api_key

    def check_params(self, params):
        # TODO: move all validity checks to another file ?
        valid_params = ['q', 'fq', 'begin_date', 'end_date', 'sort', 'fl', 'hl', 'page',
                        'facet_field', 'facet_filter']
                        
        for param in params:
            try:
                valid_params.index(param)
            except ValueError:
                # TODO: There Has To Be A Better Way
                print("Invalid NYT API query parameter:", param)
                sys.exit(1)

    # Returns number of queries left for the day
    def get_usage(self):
        r = requests.get(self.url, headers={'api-key': self.api_key})
        remaining = r.headers['X-RateLimit-Remaining-day']
        # TODO: would be nice to just print this but would that be bad for compatibility?
        return int(remaining)

    # Get headlines
    # TODO: return all data as .json is probably best approach?
    def query(self, params={}, all_pages=True):
        # TODO: change to **kwargs instead of forcing a dict?
        self.check_params(params)
        headlines = []
        max_page = 1
        if all_pages:
            max_page = 100

        for page_num in range(0, max_page):
            params['page'] = page_num
            r = requests.get(self.url, headers={'api-key': self.api_key}, params=params)
            parsed_json = json.loads(r.text)
            print(parsed_json)
            if len(parsed_json['response']['docs']) == 0:
                return headlines
            for article in parsed_json['response']['docs']:
                headlines.append(article['headline']['main'])
            time.sleep(1)

        return headlines