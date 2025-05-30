from urllib.parse import urlparse, urljoin

from validators import url as url_validate


def validate(try_url):
    print('try uuurl', try_url)
    url_object = urlparse(try_url)
    print('url_oojec', url_object)
    normalize_url = url_object._replace(path="", params="", query="", fragment="").geturl()
    if not url_validate(normalize_url):
        return False
    return normalize_url
