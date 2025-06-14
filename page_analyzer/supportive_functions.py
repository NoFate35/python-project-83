from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from validators import url as url_validate


def validate(try_url: str) -> dict:
    url_object = urlparse(try_url)
    normalize_url = url_object._replace(path="",
                                        params="",
                                        query="",
                                        fragment="").geturl()
    if not url_validate(normalize_url):
        return None
    return normalize_url


def get_response(url: str) -> dict:
    try:
        response = requests.get(url['name'])
        print("response", response)
        response.raise_for_status()
        return response
    except Exception:
        
        return None


def make_check(url_check: dict, url_response: dict) -> None:
    url_check['status_code'] = url_response.status_code
    html_doc = url_response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    url_title = soup.title
    if url_title:
        url_check['title'] = url_title.string
    url_h1 = soup.h1
    if url_h1:
        url_check['h1'] = url_h1.string
    url_meta_tags = soup.find_all('meta')
    if url_meta_tags:
        for url_meta_tag in url_meta_tags:
            url_meta_tag_attrs = url_meta_tag.attrs
            meta_tags = set(url_meta_tag_attrs.keys())
            if set(['name', 'content']).issubset(meta_tags):
                if url_meta_tag_attrs['name'] == 'description':
                    url_check['description'] = url_meta_tag_attrs['content']