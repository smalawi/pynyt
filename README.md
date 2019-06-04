# About
pynyt is a wrapper for the [New York Times Article Search API](https://developer.nytimes.com/article_search_v2.json#/README),
which enables retrieval of Times article metadata via a variety of query fields. This wrapper makes use of the
[requests](http://docs.python-requests.org/en/master/) library. pynyt is written in Python 3.

**6/3/2019: pynyt has not been updated since 2017 and is probably incompatible with the current version of the Article Search API.**

## Installation

```python
import sys

sys.path.append('path/to/pynyt'))
from pynyt import NYTArticleAPIObject
```

Accessing the Article Search API requires an API key, which can be obtained for free
[here](https://developer.nytimes.com/signup).

## Usage

Results are returned as a list of dictionaries, each list representing a page of results (10 articles per page).
The API's paginator limits results to 100 pages (or 1000 articles)—set `halt_overflow=False` to return the first
1000 results even if more exist. Set `verbose=True` to see search progress (page number) printed to the console.

Documentation of query and result fields can be found
[here](https://developer.nytimes.com/article_search_v2.json#/Documentation) (click 'Show details').

Enter any number of query parameters as keyword arguments:
```python
miner = NYTArticleAPIObject('your API key')

# get 1000 news articles from the Foreign newsdesk from 1987
results_1987 = miner.query(fq = {'source': 'New York Times',
                                 'news_desk': 'Foreign',
                                 'type_of_material': 'News'},
                           begin_date = 19870101,
                           end_date = 19871231,
                           halt_overflow = False)
                           
# get 2017 articles about the Federal Reserve with faceting by news source and day of week
results_obama = miner.query(q = 'Federal Reserve',
                            begin_date = 20170101,
                            facet_field = ['source', 
                                           'day_of_week'],
                            facet_filter = True)
```

Call `get_usage()` to get the number of remaining API calls for the day (daily limit of 1000 for a given key;
note that pagination consumes API calls).
