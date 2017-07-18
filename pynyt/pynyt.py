import requests
import json
import sys
import time
import warnings


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

        r = requests.get(self.url, headers={'api-key': self.api_key}, params=params)
        time.sleep(1)
        parsed_json = json.loads(r.text)

        if 'errors' in parsed_json:
            for error in parsed_json['errors']:
                print(error)
            sys.exit(1)
    
    def check_hits(self, params):
        r = requests.get(self.url, headers={'api-key': self.api_key}, params=params)
        time.sleep(1)
        parsed_json = json.loads(r.text)

        hits = int(parsed_json['response']['meta']['hits'])
        if hits > 1000:
            print('%d articles were found' % hits)
            sys.exit(1)

    def format_fq(self, fq):
        return fq

    # Returns number of queries left for the day
    def get_usage(self):
        r = requests.get(self.url, headers={'api-key': self.api_key})
        time.sleep(1)
        remaining = r.headers['X-RateLimit-Remaining-day']
        # TODO: would be nice to just print this but would that be bad for compatibility?
        return int(remaining)

    def prep_params(self, **kwargs):
        params = {}
        for key, value in kwargs.items():
            params[key] = value

        self.check_params(params)

        if 'fq' in params:
            params['fq'] = self.format_fq(params['fq'])

        return params

    # Get headlines
    # TODO: return all data as .json is probably best approach?
    def query(self, overflow=False, **kwargs):
        params = self.prep_params(**kwargs)
        if not overflow:
            self.check_hits(params)

        headlines = []

        for page_num in range(0, 100):
            params['page'] = page_num

            r = requests.get(self.url, headers={'api-key': self.api_key}, params=params)
            time.sleep(1) # Article Search API has rate limit of 1 query/sec
            print(r.url)
            parsed_json = json.loads(r.text)
            print(parsed_json)

            if len(parsed_json['response']['docs']) == 0: # no more results on this page - all results parsed
                return headlines

            for article in parsed_json['response']['docs']:
                headlines.append(article['headline']['main'])

        warnings.warn(("Only the first 1000 articles could be scraped, as per the API's paginator limit. "
                       "Consider narrowing your search further (e.g. by date)."))
        return headlines