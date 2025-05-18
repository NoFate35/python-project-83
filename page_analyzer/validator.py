from urllib.parse import urlparse
from validators import url
def validate(url):
    o = urlparse(url)