"""
Given a html page, retrieves all href that has a file in it or other urls to do the same
"""
import requests

from .const import URL_START_POINT


def scrap_page(url: str, folder: str):
    """ get files form url page """
    url = url if url.startswith('https') else URL_START_POINT + url
    print(url)