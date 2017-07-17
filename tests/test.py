import sys 
import os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'pynyt'))
import pynyt

api_obj = pynyt.NYTArticleAPIObject("xxxx")
headlines = api_obj.query(params={'q': 'Swarthmore College',
                                  'begin_date': '20160717'})

for headline in headlines:
    print(headline)

print(len(headlines))