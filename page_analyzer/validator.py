from urllib.parse import urlparse
from validators import url
def validate(try_url):
    url_object = urlparse(try_url)
    normalize_url = url_object.geturl()
    if not url(normalize_url):
        return True