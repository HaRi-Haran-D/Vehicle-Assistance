import urllib.request
from urllib.error import HTTPError

try:
    urllib.request.urlopen('http://127.0.0.1:8000/customer/dashboard/')
except HTTPError as e:
    with open('error.html', 'wb') as f:
        f.write(e.read())
