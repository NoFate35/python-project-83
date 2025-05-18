from urllib.parse import urlparse
def validate(url):
    o = urlparse("http://docs.python.org:80/3/library/urllib.parse.html?"
             "highlight=params#url-parsing")