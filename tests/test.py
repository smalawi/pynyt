import sys 
import os
import json

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'pynyt'))
import pynyt

api_obj = pynyt.NYTArticleAPIObject("*****")

# print(api_obj.get_usage())
results = api_obj.query(begin_date = 20170720,
                        page = 0,
                        facet_field = ['day_of_week',
                                       'sectiiion_name'])

for page in results:
    for facet in page['response']['facets']:
        print(facet)
