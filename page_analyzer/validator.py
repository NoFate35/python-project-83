from urllib.parse import urlparse
import requests
from validators import url as url_validate


def validate(try_url):
    url_object = urlparse(try_url)
    normalize_url = url_object._replace(path="",
                                        params="",
                                        query="",
                                        fragment="").geturl()
    if not url_validate(normalize_url):
        return False
    return normalize_url

def get_status(url):
    try:
        response = requests.get(url['name'])
        response.raise_for_status()
        return response.status_code
    except Exception:
        return None
