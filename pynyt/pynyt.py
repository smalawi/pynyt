import requests
import json
import sys
import time
import warnings


class NYTArticleAPIObject:
    def __init__(self, api_key):
        """Initialize NYTArticleAPIObject with user's API key.
        
        Obtain a free API key at https://developer.nytimes.com/
        """
        self.url = "http://api.nytimes.com/svc/search/v2/articlesearch.json"
        self.api_key = api_key

    def check_params(self, params):
        # Checks whether parameter names and values are valid 
        valid_params = ['q', 'fq', 'begin_date', 'end_date', 'sort', 'fl', 'hl', 'page',
                        'facet_field', 'facet_filter']
        
        # Check parameter names
        for param in params:
            try:
                valid_params.index(param)
            except ValueError:
                print("Invalid NYT API query parameter:", param)
                sys.exit(1)

        r = requests.get(self.url, headers={'api-key': self.api_key}, params=params)
        time.sleep(1)
        parsed_json = json.loads(r.text)

        # Check parameter values
        # Incorrect filter query fields do NOT throw errors
        if 'errors' in parsed_json:
            for error in parsed_json['errors']:
                print(error)
            sys.exit(1)
    
    def check_hits(self, params):
        # Ensures number of search results is no more than 1000
        # Halts program to avoid wasting daily alloted API calls
        r = requests.get(self.url, headers={'api-key': self.api_key}, params=params)
        time.sleep(1)
        parsed_json = json.loads(r.text)

        hits = int(parsed_json['response']['meta']['hits'])
        if hits > 1000:
            print('%d articles were found' % hits)
            sys.exit(1)

    def format_fq(self, fq):
        # Formats filter query field into a string for requests.get()
        fq_str = ''
        for key in fq:
            val = fq[key]
            valstr = ''
            if isinstance(val, list): # Multiple values for fq field
                for v in val:
                    valstr += str(v) + ' '
                valstr = valstr[:len(valstr) - 1]
            else:
                valstr = str(val)
            fq_str += key + ':(' + valstr + ') AND '
        print(fq_str[:len(fq_str) - 5])
        return fq_str[:len(fq_str) - 5]

    def prep_params(self, **kwargs):
        # Converts kwargs into dictionary of parameters for requests.get()
        params = {}
        for key, value in kwargs.items():
            params[key] = value

        self.check_params(params)

        if 'fq' in params:
            params['fq'] = self.format_fq(params['fq'])

        return params

    def get_usage(self):
        """ Gets number of remaining queries permitted for object's API key.

        Article Search API queries are limited to 1000 per day, so depending
        on the application it may be useful to check how many API calls are
        left for the day. Every call of requests.get() consumes a query (e.g.
        one per page in query(), one for this function, etc.)
        """
        r = requests.get(self.url, headers={'api-key': self.api_key})
        time.sleep(1)
        remaining = r.headers['X-RateLimit-Remaining-day']
        return int(remaining)

    def query(self, halt_overflow=True, **kwargs):
        """ Queries the NYT Article Search API, returns a list of dictionaries.

        The list contains one dict result for each page of the query results. The
        structure of the dictionaries match that of the API's JSON output.
        Each page contains information for up to 10 articles. The API's paginator
        is limited to 100 pages; in other words, results are limited to the
        first 1000 articles found by the query. If no page is specified, the
        program will return each page of results via the list.

        Keyword arguments:
        halt_overflow -- if true, checks whether more than 1000 articles are found
                         and if so, terminates program to avoid returning partial
                         results. (default True)
        kwargs -- arguments for search query
        """
        params = self.prep_params(**kwargs)

        try: # if page number for the query is given
            floor_page = int(params['page'])
            ceil_page = floor_page + 1
        except KeyError: # if page number is not given by user
            floor_page = 0
            ceil_page = 100
            if halt_overflow:
                self.check_hits(params)

        results = []

        for page_num in range(floor_page, ceil_page):
            params['page'] = page_num

            r = requests.get(self.url, headers={'api-key': self.api_key}, params=params)
            time.sleep(1) # Article Search API has rate limit of 1 query/sec
            print(r.url)
            parsed_json = json.loads(r.text)

            if len(parsed_json['response']['docs']) == 0: # no more results on this page -> all results parsed
                return results

            results.append(parsed_json)

        warnings.warn(("Only the first 1000 articles could be scraped, as per the API's paginator limit. "
                       "Consider narrowing your search further (e.g. by date)."))
        return results