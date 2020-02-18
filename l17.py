
from urllib import request

from http.client import HTTPResponse


with request.urlopen("http://www.baidu.com") as f :
    print(f.status)

