import sys 
import os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'pynyt'))
import pynyt

apiobj = pynyt.NYTArticleAPIObject("43207e6b68494e4184584461a82b3aa2")
print(apiobj.query(params={'paaefege': 5, 'efaefe': 'feeeee'}))